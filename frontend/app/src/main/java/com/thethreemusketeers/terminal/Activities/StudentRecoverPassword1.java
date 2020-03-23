package com.thethreemusketeers.terminal.Activities;

import android.os.Bundle;
import android.content.Intent;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.thethreemusketeers.terminal.R;
import org.json.JSONObject;


public class StudentRecoverPassword1 extends AppCompatActivity {

    EditText otpField, newPasswordEditText, confirmPasswordEditText;
    TextView attentionRequiredTowardsOtpField, attentionRequiredTowardsNewPasswordField, attentionRequiredTowardsConfirmPasswordField;
    Button saveChangesBtn;
    ImageView newPasswordEye, confirmPasswordEye;
    Boolean newEyeTogglerFlag = true, confirmEyeTogglerFlag = true;
    Boolean proceedingFlag = false, invalidAttempt = false;

    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_recover_password1);

        //Fetching XML Elements
        otpField = findViewById(R.id.otp_field);
        newPasswordEditText = findViewById(R.id.new_password_edit_text);
        confirmPasswordEditText = findViewById(R.id.confirm_password_edit_text);
        attentionRequiredTowardsOtpField = findViewById(R.id.attention_required_on_otp_editText);
        attentionRequiredTowardsNewPasswordField = findViewById(R.id.attention_required_on_new_password_editText);
        attentionRequiredTowardsConfirmPasswordField = findViewById(R.id.attention_required_on_confirm_password_editText);
        newPasswordEye = findViewById(R.id.new_password_eye);
        confirmPasswordEye = findViewById(R.id.confirm_password_eye);
        saveChangesBtn = findViewById(R.id.save_changes_btn);

        // SETTING EVENT LISTENERS

        // EYE TOGGLER FOR NEW PASSWORD FIELD
        newPasswordEye.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(newEyeTogglerFlag){
                    newPasswordEditText.setTransformationMethod(null);
                    newEyeTogglerFlag = false;
                    newPasswordEye.setImageResource(R.drawable.password_eye_crossed);
                } else{
                    newPasswordEditText.setTransformationMethod(new PasswordTransformationMethod());
                    newEyeTogglerFlag = true;
                    newPasswordEye.setImageResource(R.drawable.password_eye);
                }
            }
        }));

        // EYE TOGGLER FOR CONFIRM PASSWORD FIELD
        confirmPasswordEye.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(confirmEyeTogglerFlag){
                    confirmPasswordEditText.setTransformationMethod(null);
                    confirmEyeTogglerFlag = false;
                    confirmPasswordEye.setImageResource(R.drawable.password_eye_crossed);
                } else{
                    confirmPasswordEditText.setTransformationMethod(new PasswordTransformationMethod());
                    confirmEyeTogglerFlag = true;
                    confirmPasswordEye.setImageResource(R.drawable.password_eye);
                }
            }
        }));

        // SAVE CHANGES BUTTON CLICK LISTENER
        saveChangesBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String otpValue = otpField.getText().toString();
                String newPasswordValue = newPasswordEditText.getText().toString();
                String confirmPasswordValue = confirmPasswordEditText.getText().toString();

                if(otpValue.equals("")){
                    attentionRequiredTowardsOtpField.setAlpha(1);
//                    attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
                    attentionRequiredTowardsOtpField.setText("*Required");
                    proceedingFlag = false;
                } else{
                    attentionRequiredTowardsOtpField.setAlpha(0);
//                    proceedingFlag = true;
                }
                if(newPasswordValue.equals("")){
                    attentionRequiredTowardsNewPasswordField.setAlpha(1);
                    attentionRequiredTowardsNewPasswordField.setText("*Required");
                    proceedingFlag = false;
                } else {
                    attentionRequiredTowardsNewPasswordField.setAlpha(0);
//                    proceedingFlag = true;
                }
                if(confirmPasswordValue.equals("")){
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(1);
                    attentionRequiredTowardsConfirmPasswordField.setText("*Required");
                    proceedingFlag = false;
                } else {
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
//                    proceedingFlag = true;
                }
                if(proceedingFlag){
                    startActivity(new Intent(StudentRecoverPassword1.this, MainActivity.class));
                }
            }
        }));


    }
}

