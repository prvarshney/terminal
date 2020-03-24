package com.thethreemusketeers.terminal.Activities;

import android.os.Bundle;
import android.content.Intent;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.DefaultRetryPolicy;
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
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class StudentRecoverPassword1 extends AppCompatActivity {

    EditText otpField, newPasswordEditText, confirmPasswordEditText;
    TextView attentionRequiredTowardsOtpField, attentionRequiredTowardsNewPasswordField, attentionRequiredTowardsConfirmPasswordField;
    TextView attentionRequiredTowardsInvalid;
    View saveChangesBtn;
    ImageView newPasswordEye, confirmPasswordEye;
    Boolean newEyeTogglerFlag = true, confirmEyeTogglerFlag = true;
    Boolean mismatchFlag = false, invalidAttemptFlag = false;
    Boolean isOtpEmptyFlag = false, isNewPasswordEmptyFlag = false, isConfirmPasswordEmpty = false;

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

        // ADDING TEXT WATCHER ON OTP, New PASSWORD AND CONFIRM PASSWORD FIELD
        otpField.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(invalidAttemptFlag){
                    attentionRequiredTowardsInvalid.setAlpha(0);
                    invalidAttemptFlag = false;
                }
                if(isOtpEmptyFlag){
                    attentionRequiredTowardsOtpField.setAlpha(0);
                    isOtpEmptyFlag = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        newPasswordEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(isNewPasswordEmptyFlag){
                    attentionRequiredTowardsNewPasswordField.setAlpha(0);
                    isNewPasswordEmptyFlag = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        confirmPasswordEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(mismatchFlag){
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                    mismatchFlag = false;
                }
                if(isConfirmPasswordEmpty){
                    attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                    isConfirmPasswordEmpty = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        // CHECK THE CREDENTAILS ENTERED BY THE USER.
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = Config.HostURL + "/student/recover_password/verify_otp";

        // SAVE CHANGES BUTTON CLICK LISTENER
        saveChangesBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveChangesBtn.setClickable(false);
                String otpValue = otpField.getText().toString();
                final String newPasswordValue = newPasswordEditText.getText().toString();
                final String confirmPasswordValue = confirmPasswordEditText.getText().toString();

                if(!otpValue.equals("") && !newPasswordValue.equals("") && !confirmPasswordValue.equals("") && (newPasswordValue.equals(confirmPasswordValue))){
                    final ProgressButton progressButton = new ProgressButton(StudentRecoverPassword1.this,saveChangesBtn);
                    progressButton.buttonProgressActivatedState("Please Wait...");

                    // SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED PASSWORD
                    // EXISTS OR NOT
                    Map<String, String> postParameters = new HashMap<>();
                    postParameters.put("user_id", StudentForgotPasswordObject.userid);
                    postParameters.put("otp", otpValue);
                    postParameters.put("new_password",newPasswordValue);

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                                    Gson gson = new Gson();
                                    saveChangesBtn.setClickable(true);
                                    progressButton.buttonProgressStoppedState("SAVE CHANGES");
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(), MessageAndStatusResponse.class);
                                    if (res.status == 401 || res.status==204 ) {
                                        invalidAttemptFlag = true;
                                        attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                                        attentionRequiredTowardsInvalid.setText("*Invalid OTP Combination");
                                        attentionRequiredTowardsInvalid.setAlpha(1);
                                    } else if (res.status == 301) {
                                        attentionRequiredTowardsInvalid.setAlpha(0);
                                            invalidAttemptFlag = false;
                                            startActivity(new Intent(StudentRecoverPassword1.this, MainActivity.class));
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
                    requestObject.setRetryPolicy(new DefaultRetryPolicy(20000,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
                    requestQueue.add(requestObject);
                } else {
                    saveChangesBtn.setClickable(true);
                    if (otpValue.equals("")) {
                        attentionRequiredTowardsOtpField.setAlpha(1);
                        attentionRequiredTowardsOtpField.setText("*Required");
                        isOtpEmptyFlag = true;
                    } else {
                        attentionRequiredTowardsOtpField.setAlpha(0);
                    }
                    if (newPasswordValue.equals("")) {
                        attentionRequiredTowardsNewPasswordField.setAlpha(1);
                        attentionRequiredTowardsNewPasswordField.setText("*Required");
                        isNewPasswordEmptyFlag = true;
                    } else {
                        attentionRequiredTowardsNewPasswordField.setAlpha(0);
                    }
                    if (confirmPasswordValue.equals("")) {
                        attentionRequiredTowardsConfirmPasswordField.setAlpha(1);
                        attentionRequiredTowardsConfirmPasswordField.setText("*Required");
                        isConfirmPasswordEmpty = true;
                    } else {
                        attentionRequiredTowardsConfirmPasswordField.setAlpha(0);
                    }
                    if(!newPasswordValue.equals(confirmPasswordValue)){
                        mismatchFlag = true;
                        attentionRequiredTowardsConfirmPasswordField.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                        attentionRequiredTowardsConfirmPasswordField.setText("*Password Mismatch");
                        attentionRequiredTowardsConfirmPasswordField.setAlpha(1);
                    }
                }
            }
        }));


    }
}

