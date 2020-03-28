package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.style.ClickableSpan;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.ProfileCreationSuccess;
import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class CreateProfile5 extends AppCompatActivity {

    // DECLARING VARIABLES AND OBJECTS
    TextView resendOTPTextView, attentionReqOnEmailOtpTextView, attentionReqOnSMSOtpTextView;
    View nextBtn;
    EditText emailOTPEditText, smsOTPEditText;
    Boolean isEmailVerified = false, isPhoneNumberVerified = false, isEmailOTPTextViewEmpty = true, isSMSOTPTextViewEmpty = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile5);

        // FETCHING ELEMENTS FROM XML DESIGN
        nextBtn = findViewById(R.id.activity5_next_btn);
        resendOTPTextView = findViewById(R.id.resend_otp_text_view);
        attentionReqOnEmailOtpTextView = findViewById(R.id.attention_required_on_email_otp_editText);
        attentionReqOnSMSOtpTextView = findViewById(R.id.attention_required_on_sms_otp_editText);
        emailOTPEditText = findViewById(R.id.email_otp);
        smsOTPEditText = findViewById(R.id.sms_otp);

        // ADDING CLICKABLE SPAN FOR RESEND OTP LINK
        SpannableString resendOTPText = new SpannableString("Doesn't Receive OTPs? Resend them.");
        ClickableSpan otpResendLink = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // RESEND OTP FOR CURRENT USER
            }
            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
                ds.setTypeface(Typeface.DEFAULT_BOLD);
            }
        };
        resendOTPText.setSpan(otpResendLink,21,34, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        resendOTPTextView.setText(resendOTPText);

        // ADDING EVENT LISTENERS ON CLICKABLE ITEMS
        // CREATING REQUEST QUEUE
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        // CREATING EMAIL VERIFICATION REQUEST URLS BASED ON ACCOUNT TYPE
        final String emailVerificationReqURL =  (UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)))
                ? Config.HostURL + "/faculty/verify_email"
                : Config.HostURL + "/student/verify_email";
        // CREATING PHONE VERIFICATION REQUEST URLS BASED ON ACCOUNT TYPE
        final String phoneVerificationReqURL = (UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)))
                ? Config.HostURL + "/faculty/verify_phone"
                : Config.HostURL + "/student/verify_phone";

        // ADDING EVENT LISTENER ON NEXT BUTTON
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // CHANGING STATE OF PROGRESS BUTTON FROM NEXT TO PLEASE WAIT
                final ProgressButton progressButton = new ProgressButton(CreateProfile5.this,nextBtn);
                progressButton.buttonProgressActivatedState("Please Wait...");
                // CHECKING EMAIL OTP INPUT FIELD ISN'T EMPTY
                if ( emailOTPEditText.getText().toString().equals("") ) {
                    isEmailOTPTextViewEmpty = true;
                    attentionReqOnEmailOtpTextView.setText("*Required");
                    attentionReqOnEmailOtpTextView.setAlpha(1);
                }
                else {
                    isEmailOTPTextViewEmpty = false;
                    attentionReqOnEmailOtpTextView.setAlpha(0);
                }
                // CHECKING SMS OTP INPUT FIELD ISN'T EMPTY
                if ( smsOTPEditText.getText().toString().equals("") ) {
                    isSMSOTPTextViewEmpty = true;
                    attentionReqOnSMSOtpTextView.setText("*Required");
                    attentionReqOnSMSOtpTextView.setAlpha(1);
                }
                else {
                    isSMSOTPTextViewEmpty = false;
                    attentionReqOnSMSOtpTextView.setAlpha(0);
                }

                // EXECUTES WHEN BOTH OTP FIELDS AREN'T EMPTY
                if ( !isEmailOTPTextViewEmpty && !isSMSOTPTextViewEmpty ) {
                    // CREATING REQUEST OBJECT FOR EMAIL VERIFICATION LINK
                    Map<String,String> postParametersOfVerifyEmail = new HashMap<String,String>();
                    postParametersOfVerifyEmail.put("email_id", UserRegisterObject.email);
                    postParametersOfVerifyEmail.put("phone_number", UserRegisterObject.phone_number);
                    postParametersOfVerifyEmail.put("email_otp", emailOTPEditText.getText().toString());

                    // CREATING REQUEST OBJECT FOR PHONE VERIFICATION LINK
                    Map<String,String> postParametersOfVerifySMS = new HashMap<String,String>();
                    postParametersOfVerifySMS.put("email_id",UserRegisterObject.email);
                    postParametersOfVerifySMS.put("phone_number",UserRegisterObject.phone_number);
                    postParametersOfVerifySMS.put("sms_otp",smsOTPEditText.getText().toString());

                    // IF ACCOUNT-TYPE IS FACULTY INSERTING HIS/HER FACULTY_ID
                    if (UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty))) {
                        postParametersOfVerifyEmail.put("faculty_id", UserRegisterObject.faculty_id);
                        postParametersOfVerifySMS.put("faculty_id",UserRegisterObject.faculty_id);
                    }
                    // IF ACCOUNT-TYPE IS STUDENT INSERTING HIS/HER ENROLLMENT
                    else if(UserRegisterObject.account_type.equals(getString(R.string.account_type_student))) {
                        postParametersOfVerifyEmail.put("enrollment", UserRegisterObject.enrollment);
                        postParametersOfVerifySMS.put("enrollment",UserRegisterObject.enrollment);
                    }

                    // JSON REQUEST OBJECT FOR EMAIL VERIFICATION ROUTE
                    JsonObjectRequest requestObjectOfVerifyEmail = new JsonObjectRequest(
                            Request.Method.POST,
                            emailVerificationReqURL,
                            new JSONObject(postParametersOfVerifyEmail),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(),MessageAndStatusResponse.class);
                                    if ( res.status == 200 ) {
                                        isEmailVerified = true;
                                        attentionReqOnEmailOtpTextView.setText("*Verified");
                                        attentionReqOnEmailOtpTextView.setAlpha(1);

                                        // STARTING NEW ACTIVITY WHEN BOTH FIELDS ARE VERIFIED
                                        if ( isEmailVerified && isPhoneNumberVerified ) 
                                            startActivity( new Intent(CreateProfile5.this, ProfileCreationSuccess.class) );
                                    }
                                    else if ( res.status == 401 ) {
                                        isEmailVerified = false;
                                        attentionReqOnEmailOtpTextView.setText("*Invalid");
                                        attentionReqOnEmailOtpTextView.setAlpha(1);
                                        progressButton.buttonProgressStoppedState("NEXT");
                                    }
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            }
                    );

                    // JSON REQUEST OBJECT FOR PHONE VERIFICATION LINK
                    JsonObjectRequest requestObjectOfVerifyPhone = new JsonObjectRequest(
                            Request.Method.POST,
                            phoneVerificationReqURL,
                            new JSONObject(postParametersOfVerifySMS),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(),MessageAndStatusResponse.class);
                                    if ( res.status == 200 ) {
                                        isPhoneNumberVerified = true;
                                        attentionReqOnSMSOtpTextView.setText("*Verified");
                                        attentionReqOnSMSOtpTextView.setAlpha(1);

                                        // STARTING NEW ACTIVITY WHEN BOTH FIELDS ARE VERIFIED
                                        if ( isEmailVerified && isPhoneNumberVerified ) {
                                            startActivity( new Intent(CreateProfile5.this, ProfileCreationSuccess.class) );
                                        }
                                        else {
                                            progressButton.buttonProgressStoppedState("NEXT");
                                        }
                                    }
                                    else if ( res.status == 401 ) {
                                        isPhoneNumberVerified = false;
                                        attentionReqOnSMSOtpTextView.setText("*Invalid");
                                        attentionReqOnSMSOtpTextView.setAlpha(1);
                                        progressButton.buttonProgressStoppedState("NEXT");
                                    }
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            }
                    );

                    // ADDING REQUEST OBJECTS IN REQUEST QUEUE
                    if ( !isEmailVerified )
                        requestQueue.add(requestObjectOfVerifyEmail);
                    if ( !isPhoneNumberVerified )
                        requestQueue.add(requestObjectOfVerifyPhone);
                }
                else {
                    progressButton.buttonProgressStoppedState("NEXT");
                }

            }
        });
    }
}
