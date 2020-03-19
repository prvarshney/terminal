package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Typeface;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.style.ClickableSpan;
import android.view.View;
import android.widget.Button;
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
import com.thethreemusketeers.terminal.JSONRequestObject.FacultyRegisterObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class CreateProfile5 extends AppCompatActivity {

    TextView resendOTPTextView, attentionReqOnEmailOtpTextView, attentionReqOnSMSOtpTextView;
    Button nextBtn;
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

        // ADDING EVENT LISTENERS
        // CREATING REQUEST QUEUE
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String emailVerificationReqURL = Config.HostURL + "/faculty/verify_email";
        final String phoneVerificationReqURL = Config.HostURL + "/faculty/verify_phone";

        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // CHECKING WHETHER INPUT FIELDS AREN'T EMPTY
                if ( emailOTPEditText.getText().toString().equals("") ) {
                    isEmailOTPTextViewEmpty = true;
                    attentionReqOnEmailOtpTextView.setText("*Required");
                    attentionReqOnEmailOtpTextView.setAlpha(1);
                }
                else {
                    isEmailOTPTextViewEmpty = false;
                    attentionReqOnEmailOtpTextView.setAlpha(0);
                }
                if ( smsOTPEditText.getText().toString().equals("") ) {
                    isSMSOTPTextViewEmpty = true;
                    attentionReqOnSMSOtpTextView.setText("*Required");
                    attentionReqOnSMSOtpTextView.setAlpha(1);
                }
                else {
                    isSMSOTPTextViewEmpty = false;
                    attentionReqOnSMSOtpTextView.setAlpha(0);
                }

                if ( !isEmailOTPTextViewEmpty && !isSMSOTPTextViewEmpty ) {

                    // CREATING REQUEST OBJECT FOR EMAIL VERIFICATION LINK AND PHONE VERIFICATION LINK
                    Map<String,String> postParametersOfVerifyEmail = new HashMap<String,String>();
                    postParametersOfVerifyEmail.put("email_id", FacultyRegisterObject.email);
                    postParametersOfVerifyEmail.put("faculty_id", FacultyRegisterObject.faculty_id);
                    postParametersOfVerifyEmail.put("phone_number", FacultyRegisterObject.phone_number);
                    postParametersOfVerifyEmail.put("email_otp", emailOTPEditText.getText().toString());

                    Map<String,String> postParametersOfVerifySMS = new HashMap<String,String>();
                    postParametersOfVerifySMS.put("email_id",FacultyRegisterObject.email);
                    postParametersOfVerifySMS.put("faculty_id",FacultyRegisterObject.faculty_id);
                    postParametersOfVerifySMS.put("phone_number",FacultyRegisterObject.phone_number);
                    postParametersOfVerifySMS.put("sms_otp",smsOTPEditText.getText().toString());

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
                                    }
                                    else if ( res.status == 401 ) {
                                        isEmailVerified = false;
                                        attentionReqOnEmailOtpTextView.setText("*Invalid");
                                        attentionReqOnEmailOtpTextView.setAlpha(1);
                                    }
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {

                                }
                            }
                    );

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
                                    }
                                    else if ( res.status == 401 ) {
                                        isPhoneNumberVerified = false;
                                        attentionReqOnSMSOtpTextView.setText("*Invalid");
                                        attentionReqOnSMSOtpTextView.setAlpha(1);
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
                    requestQueue.add(requestObjectOfVerifyEmail);
                    requestQueue.add(requestObjectOfVerifyPhone);
                }

            }
        });
    }
}
