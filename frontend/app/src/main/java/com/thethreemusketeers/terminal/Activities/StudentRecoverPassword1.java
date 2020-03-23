package com.thethreemusketeers.terminal.Activities;

import android.os.Bundle;
import android.content.Intent;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.JSONRequestObject.StudentForgotPasswordObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.R;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class StudentRecoverPassword1 extends AppCompatActivity {

    EditText otpField, newPasswordEditText, confirmPasswordEditText;
    TextView attentionRequiredTowardsOtpField, attentionRequiredTowardsNewPasswordField, attentionRequiredTowardsConfirmPasswordField;
    TextView attentionRequiredTowardsInvalid;
    Button saveChangesBtn;
    ImageView newPasswordEye, confirmPasswordEye;
    Boolean newEyeTogglerFlag = true, confirmEyeTogglerFlag = true;
    Boolean proceedingFlag = false, invalidAttemptFlag = false;

    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_recover_password1);

        //Fetching XML Elements
        otpField = findViewById(R.id.otp_field);
        newPasswordEditText = findViewById(R.id.new_password_edit_text);
        confirmPasswordEditText = findViewById(R.id.confirm_password_edit_text);
        attentionRequiredTowardsOtpField = findViewById(R.id.attention_required_on_otp_editText);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_on_otp_editText);
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

        // CHECK THE CREDENTAILS ENTERED BY THE USER.
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = Config.HostURL + "/student/recover_password/verify_otp";

        // SAVE CHANGES BUTTON CLICK LISTENER
        saveChangesBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String otpValue = otpField.getText().toString();
                final String newPasswordValue = newPasswordEditText.getText().toString();
                final String confirmPasswordValue = confirmPasswordEditText.getText().toString();

                if(!otpValue.equals("") && !newPasswordValue.equals("") && !confirmPasswordValue.equals("")){
                    // SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED PASSWORD
                    // EXISTS OR NOT
                    Map<String, String> postParameters = new HashMap<>();
                    postParameters.put("user_id", StudentForgotPasswordObject.userid);
                    postParameters.put("otp", otpField.getText().toString());
                    postParameters.put("new_password",newPasswordValue);

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(), MessageAndStatusResponse.class);
                                    if (res.status == 401 || res.status==204 ) {
                                        invalidAttemptFlag = true;
                                        attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                                        attentionRequiredTowardsInvalid.setText("*Invalid OTP Combination");
                                        attentionRequiredTowardsInvalid.setAlpha(1);
                                        proceedingFlag = false;
                                    } else if (res.status == 301) {
                                        attentionRequiredTowardsInvalid.setAlpha(0);
                                        if(newPasswordValue.equals(confirmPasswordValue)){
                                            attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                                            invalidAttemptFlag = false;
                                            startActivity(new Intent(StudentRecoverPassword1.this, MainActivity.class));
                                        } else {
                                            invalidAttemptFlag = true;
                                            attentionRequiredTowardsConfirmPasswordField.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                                            attentionRequiredTowardsConfirmPasswordField.setText("*Password Mismatch");
                                            attentionRequiredTowardsConfirmPasswordField.setAlpha(1);
                                            proceedingFlag = false;
                                        }

                                    }
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    Log.e("Response", error.toString());
                                }
                            }
                    );
                    requestQueue.add(requestObject);
                }

                if(otpValue.equals("")){
                    attentionRequiredTowardsOtpField.setAlpha(1);
                    attentionRequiredTowardsOtpField.setText("*Required");
                    proceedingFlag = false;
                } else{
                    attentionRequiredTowardsOtpField.setAlpha(0);
                }
                if(newPasswordValue.equals("")){
                    attentionRequiredTowardsNewPasswordField.setAlpha(1);
                    attentionRequiredTowardsNewPasswordField.setText("*Required");
                    proceedingFlag = false;
                } else {
                    attentionRequiredTowardsNewPasswordField.setAlpha(0);
                }
                if(confirmPasswordValue.equals("")){
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(1);
                    attentionRequiredTowardsConfirmPasswordField.setText("*Required");
                    proceedingFlag = false;
                } else {
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                }
                if(proceedingFlag){
                    startActivity(new Intent(StudentRecoverPassword1.this, MainActivity.class));
                }
            }
        }));


    }
}

