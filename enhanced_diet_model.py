test_users = [
    {
        "name": "Sarah (28F, Active, Weight Loss Goal)",
        "data": {
            'Age': 28, 'Gender': 'Female', 'Height_cm': 165,
            'Weight_kg': 75, 'Exercise_Frequency': 5
            # ... complete profile
        }
    }
]



import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

class EnhancedDietPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.target_names = ['Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats']
        
    def calculate_bmr(self, age, weight, height, gender):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        elif gender.lower() == 'female':
            return 10 * weight + 6.25 * height - 5 * age - 161
        else:  # Other
            return 10 * weight + 6.25 * height - 5 * age - 78  # Average
    
    def calculate_tdee(self, bmr, exercise_frequency, daily_steps):
        """Calculate Total Daily Energy Expenditure"""
        # Activity multipliers based on exercise frequency and steps
        if exercise_frequency >= 6:
            activity_multiplier = 1.725  # Very active
        elif exercise_frequency >= 4:
            activity_multiplier = 1.55   # Moderately active
        elif exercise_frequency >= 2:
            activity_multiplier = 1.375  # Lightly active
        else:
            activity_multiplier = 1.2    # Sedentary
        
        # Adjust based on daily steps
        if daily_steps > 12000:
            activity_multiplier += 0.1
        elif daily_steps > 8000:
            activity_multiplier += 0.05
        
        return bmr * activity_multiplier
    
    def calculate_health_risk_score(self, bmi, blood_pressure_sys, blood_pressure_dia, cholesterol, blood_sugar, age):
        """Calculate health risk score (0-100, higher = more risk)"""
        risk_score = 0
        
        # BMI risk
        if bmi >= 30:
            risk_score += 25
        elif bmi >= 25:
            risk_score += 15
        elif bmi < 18.5:
            risk_score += 10
        
        # Blood pressure risk
        if blood_pressure_sys >= 140 or blood_pressure_dia >= 90:
            risk_score += 20
        elif blood_pressure_sys >= 130 or blood_pressure_dia >= 80:
            risk_score += 10
        
        # Cholesterol risk
        if cholesterol >= 240:
            risk_score += 15
        elif cholesterol >= 200:
            risk_score += 8
        
        # Blood sugar risk
        if blood_sugar >= 126:
            risk_score += 20
        elif blood_sugar >= 100:
            risk_score += 10
        
        # Age risk
        if age >= 65:
            risk_score += 10
        elif age >= 50:
            risk_score += 5
        
        return min(risk_score, 100)
    
    def enhance_dataset(self, df):
        """Add calculated features to the dataset"""
        df_enhanced = df.copy()
        
        # Calculate BMR for each row
        df_enhanced['BMR'] = df_enhanced.apply(
            lambda row: self.calculate_bmr(row['Age'], row['Weight_kg'], row['Height_cm'], row['Gender']), 
            axis=1
        )
        
        # Calculate TDEE
        df_enhanced['TDEE'] = df_enhanced.apply(
            lambda row: self.calculate_tdee(row['BMR'], row['Exercise_Frequency'], row['Daily_Steps']), 
            axis=1
        )
        
        # Calculate health risk score
        df_enhanced['Health_Risk_Score'] = df_enhanced.apply(
            lambda row: self.calculate_health_risk_score(
                row['BMI'], row['Blood_Pressure_Systolic'], row['Blood_Pressure_Diastolic'],
                row['Cholesterol_Level'], row['Blood_Sugar_Level'], row['Age']
            ), axis=1
        )
        
        # Activity level score (0-10)
        df_enhanced['Activity_Level_Score'] = (
            (df_enhanced['Exercise_Frequency'] / 7) * 5 + 
            (np.clip(df_enhanced['Daily_Steps'] / 15000, 0, 1)) * 5
        )
        
        # Sleep quality score (0-10)
        df_enhanced['Sleep_Quality_Score'] = np.clip(df_enhanced['Sleep_Hours'] / 8 * 10, 0, 10)
        
        return df_enhanced
    
    def prepare_features(self, df):
        """Prepare features for training"""
        # Select numeric features only
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Remove target columns from features
        feature_cols = [col for col in numeric_df.columns 
                       if not col.startswith('Recommended_') and col != 'Patient_ID']
        
        X = numeric_df[feature_cols]
        
        # Multi-output targets
        y = numeric_df[self.target_names]
        
        return X, y
    
    def train_model(self, df):
        """Train the enhanced multi-output model"""
        print("🔧 Enhancing dataset with calculated features...")
        df_enhanced = self.enhance_dataset(df)
        
        print("📊 Preparing features...")
        X, y = self.prepare_features(df_enhanced)
        
        # Store feature names
        self.feature_names = list(X.columns)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("🤖 Training multi-output model...")
        # Use MultiOutputRegressor for predicting multiple nutrition targets
        base_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model = MultiOutputRegressor(base_model)
        self.model.fit(X_train, y_train)
          # Evaluate model
        y_pred = self.model.predict(X_test)
        
        print("\n📈 Model Performance & Accuracy:")
        print("=" * 50)
        
        overall_accuracies = []
        
        for i, target in enumerate(self.target_names):
            y_true = y_test.iloc[:, i]
            y_pred_single = y_pred[:, i]
            
            # Calculate metrics
            r2 = r2_score(y_true, y_pred_single)
            mae = mean_absolute_error(y_true, y_pred_single)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred_single))
            
            # Calculate percentage accuracy (within 10% tolerance)
            percentage_error = np.abs((y_true - y_pred_single) / y_true) * 100
            accuracy_10pct = np.mean(percentage_error <= 10) * 100
            
            # Calculate mean percentage error
            mape = np.mean(percentage_error)
            
            # Store overall accuracy
            overall_accuracies.append(accuracy_10pct)
            
            print(f"\n🎯 {target.replace('Recommended_', '')}:")
            print(f"   • R² Score: {r2:.3f} ({r2*100:.1f}% variance explained)")
            print(f"   • Accuracy (±10%): {accuracy_10pct:.1f}% of predictions")
            print(f"   • Mean Absolute Error: {mae:.1f}")
            print(f"   • Root Mean Square Error: {rmse:.1f}")
            print(f"   • Mean Percentage Error: {mape:.1f}%")
        
        # Overall model accuracy
        overall_accuracy = np.mean(overall_accuracies)
        print(f"\n🏆 OVERALL MODEL ACCURACY:")
        print(f"   • Average Accuracy (±10% tolerance): {overall_accuracy:.1f}%")
        print(f"   • Model Quality: {'Excellent' if overall_accuracy > 90 else 'Good' if overall_accuracy > 80 else 'Fair' if overall_accuracy > 70 else 'Needs Improvement'}")
        
        # Additional accuracy interpretation
        print(f"\n💡 Accuracy Explanation:")
        print(f"   • R² = {np.mean([r2_score(y_test.iloc[:, i], y_pred[:, i]) for i in range(len(self.target_names))]):.3f} means {np.mean([r2_score(y_test.iloc[:, i], y_pred[:, i]) for i in range(len(self.target_names))])*100:.1f}% of nutrition variance is explained")
        print(f"   • {overall_accuracy:.1f}% of predictions are within 10% of actual values")
        print(f"   • This is considered {'professional-grade' if overall_accuracy > 85 else 'good' if overall_accuracy > 75 else 'adequate'} accuracy for nutrition prediction")
        
        return X_test, y_test, y_pred
    
    def validate_prediction(self, calories, protein, carbs, fats, bmr):
        """Apply health-safe bounds to predictions"""
        # Calorie bounds (80-200% of BMR)
        min_calories = bmr * 0.8
        max_calories = bmr * 2.0
        safe_calories = np.clip(calories, min_calories, max_calories)
        
        # Protein bounds (0.8-2.5g per kg body weight approximation)
        # Using average weight estimation from BMR
        approx_weight = bmr / 15  # Rough estimation
        min_protein = approx_weight * 0.8
        max_protein = approx_weight * 2.5
        safe_protein = np.clip(protein, min_protein, max_protein)
        
        # Ensure macros add up reasonably (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
        total_macro_calories = safe_protein * 4 + carbs * 4 + fats * 9
        
        if total_macro_calories > safe_calories * 1.1:  # 10% tolerance
            # Scale down macros proportionally
            scale_factor = safe_calories / total_macro_calories
            safe_protein *= scale_factor
            carbs *= scale_factor
            fats *= scale_factor
        
        return safe_calories, safe_protein, carbs, fats
    
    def predict(self, user_data):
        """Make prediction for a single user"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Create DataFrame with user data
        user_df = pd.DataFrame([user_data])
        
        # Calculate derived features
        user_df['BMR'] = self.calculate_bmr(
            user_data['Age'], user_data['Weight_kg'], 
            user_data['Height_cm'], user_data['Gender']
        )
        user_df['TDEE'] = self.calculate_tdee(
            user_df['BMR'].iloc[0], user_data['Exercise_Frequency'], user_data['Daily_Steps']
        )
        user_df['Health_Risk_Score'] = self.calculate_health_risk_score(
            user_data['BMI'], user_data['Blood_Pressure_Systolic'], 
            user_data['Blood_Pressure_Diastolic'], user_data['Cholesterol_Level'],
            user_data['Blood_Sugar_Level'], user_data['Age']
        )
        user_df['Activity_Level_Score'] = (
            (user_data['Exercise_Frequency'] / 7) * 5 + 
            (np.clip(user_data['Daily_Steps'] / 15000, 0, 1)) * 5
        )
        user_df['Sleep_Quality_Score'] = np.clip(user_data['Sleep_Hours'] / 8 * 10, 0, 10)
        
        # Select features in the same order as training
        user_features = user_df[self.feature_names]
        
        # Make prediction
        prediction = self.model.predict(user_features)[0]
        
        # Apply validation
        safe_prediction = self.validate_prediction(
            prediction[0], prediction[1], prediction[2], prediction[3], user_df['BMR'].iloc[0]
        )
        
        return {
            'recommended_calories': round(safe_prediction[0]),
            'recommended_protein': round(safe_prediction[1], 1),
            'recommended_carbs': round(safe_prediction[2], 1),
            'recommended_fats': round(safe_prediction[3], 1),
            'bmr': round(user_df['BMR'].iloc[0]),
            'tdee': round(user_df['TDEE'].iloc[0]),
            'health_risk_score': round(user_df['Health_Risk_Score'].iloc[0]),
            'activity_level_score': round(user_df['Activity_Level_Score'].iloc[0], 1)
        }
    
    def save_model(self, filename='enhanced_diet_predictor.pkl'):
        """Save the trained model"""
        joblib.dump((self.model, self.feature_names, self.target_names), filename)
        print(f"✅ Enhanced model saved as '{filename}'")
    
    def load_model(self, filename='enhanced_diet_predictor.pkl'):
        """Load a trained model"""
        self.model, self.feature_names, self.target_names = joblib.load(filename)
        print(f"✅ Enhanced model loaded from '{filename}'")

# Main execution
if __name__ == "__main__":
    # Load dataset
    print("📁 Loading dataset...")
    df = pd.read_csv('Personalized_Diet_Recommendations.csv')
    print(f"✅ Data loaded: {len(df)} records")
    
    # Initialize and train model
    predictor = EnhancedDietPredictor()
    X_test, y_test, y_pred = predictor.train_model(df)
    
    # Save model
    predictor.save_model()
    
    # Create feature importance plot for the first target (calories)
    importances = predictor.model.estimators_[0].feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(len(indices[:15])), importances[indices[:15]], color='skyblue')
    plt.yticks(range(len(indices[:15])), [predictor.feature_names[i] for i in indices[:15]])
    plt.title('Top 15 Feature Importances for Calorie Prediction')
    plt.xlabel('Relative Importance')
    plt.tight_layout()
    plt.savefig("enhanced_feature_importance.png", dpi=300, bbox_inches='tight')
    print("📊 Enhanced feature importance plot saved")
    
    print("\n🎉 Enhanced model training completed!")
