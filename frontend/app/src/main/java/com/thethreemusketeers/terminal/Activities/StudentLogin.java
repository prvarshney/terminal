package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.Editable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.TextWatcher;
import android.text.method.LinkMovementMethod;
import android.text.method.PasswordTransformationMethod;
import android.text.style.ClickableSpan;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusTokenResponse;
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class StudentLogin extends AppCompatActivity {

    Spinner accountTypeDropdown;
    EditText passwordEditText, userId ;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsPasswordTypeField,attentionRequiredTowardsInvalid, forgotLink, signupLink;
    ImageView passwordEye;
    Boolean eyeTogglerFlag = true, proceedingUsernameFlag=false, proceedingPasswordFlag=false, invalidAttemptFlag = false;
    View loginBtn;
    Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login);

        //Fetching XML Elements
        forgotLink = findViewById(R.id.forgot_link);
        signupLink = findViewById(R.id.signup_link);
        accountTypeDropdown = findViewById(R.id.account_type_dropdown);
        passwordEditText = findViewById(R.id.password_edit_text);
        passwordEye = findViewById(R.id.password_eye);
        userId = findViewById(R.id.userid);
        loginBtn = findViewById(R.id.login_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsPasswordTypeField = findViewById(R.id.attention_required_on_password_editText);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_on_username_editText);

        //SETTING DROPDOWN ELEMENTS
        String[] accountTypeDropdownElements = new String[]{"Change Account Type","Faculty"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, R.layout.spinner_dropdown, accountTypeDropdownElements){
            public boolean isEnabled(int position){
                if(position==0){
                    return  false;
                } else {
                    return true;
                }
            }
        };
        adapter.setDropDownViewResource(R.layout.spinner_text);
        accountTypeDropdown.setAdapter(adapter);
        accountTypeDropdown.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener()
        {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View view, int position, long id)
            {
                switch(position)
                {
                    case 0:
                        break;
                    case 1:
                        startActivity(new Intent(StudentLogin.this, FacultyLogin.class));
                        break;
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {

            }
        });

        //CLICKABLE SPAN
        SpannableString forgotPassword = new SpannableString("Forgotten your login details? Get help with signin.");
        SpannableString signup = new SpannableString("Don't have an account? Sign up.");
        ClickableSpan clickableSpanForgotPassword = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                //launch forgot password activity
                startActivity(new Intent(StudentLogin.this, StudentRecoverPassword1.class));
            }
            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
                ds.setTypeface(Typeface.DEFAULT_BOLD);
            }
        };

        ClickableSpan clickableSpanSignup = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // LAUNCH CREATE ACCOUNT ACTIVITY
                startActivity(new Intent(StudentLogin.this, StudentRecoverPassword2.class));
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
                ds.setTypeface(Typeface.DEFAULT_BOLD);
            }
        };

        forgotPassword.setSpan(clickableSpanForgotPassword,30,51,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        signup.setSpan(clickableSpanSignup,22,31,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        forgotLink.setText(forgotPassword);
        forgotLink.setMovementMethod(LinkMovementMethod.getInstance());
        signupLink.setText(signup);
        signupLink.setMovementMethod(LinkMovementMethod.getInstance());

        // CHECK THE CREDENTAILS ENTERED BY THE USER.
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = Config.HostURL + "/student/login";

        // SETTING EVENT LISTENERS
        passwordEye.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(eyeTogglerFlag){
                    passwordEditText.setTransformationMethod(null);
                    eyeTogglerFlag = false;
                    passwordEye.setImageResource(R.drawable.ic_password_eye_crossed_image);
                } else{
                    passwordEditText.setTransformationMethod(new PasswordTransformationMethod());
                    eyeTogglerFlag = true;
                    passwordEye.setImageResource(R.drawable.ic_password_eye_image);
                }
            }
        }));

        // ADDING TEXT WATCHER ON ENROLLMENT AND PASSWORD FIELD
        userId.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(invalidAttemptFlag){
                    attentionRequiredTowardsInvalid.setAlpha(0);
                    invalidAttemptFlag = false;
                }
                attentionRequiredTowardsUsernameField.setAlpha(0);
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });
        passwordEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(invalidAttemptFlag){
                    attentionRequiredTowardsInvalid.setAlpha(0);
                    invalidAttemptFlag = false;
                }
                attentionRequiredTowardsPasswordTypeField.setAlpha(0);
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        loginBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                 final String usernameValue = userId.getText().toString();
                 final String passwordValue = passwordEditText.getText().toString();

                if(!passwordValue.equals("") && (!usernameValue.equals(""))){
                    final ProgressButton progressButton = new ProgressButton(StudentLogin.this, loginBtn);
                    progressButton.buttonProgressActivatedState("Please Wait...");
                        // SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED PASSWORD
                        // EXISTS OR NOT
                    Map<String, String> postParameters = new HashMap<String, String>();
                        postParameters.put("password", passwordEditText.getText().toString());
                        postParameters.put("user_id",usernameValue);

                        JsonObjectRequest requestObject = new JsonObjectRequest(
                                Request.Method.POST,
                                ReqURL,
                                new JSONObject(postParameters),
                                new Response.Listener<JSONObject>() {
                                    @Override
                                    public void onResponse(JSONObject response) {
                                        Gson gson = new Gson();
                                        loginBtn.setClickable(true);
                                        progressButton.buttonProgressStoppedState("Login");
                                        MessageStatusTokenResponse res = gson.fromJson(response.toString(), MessageStatusTokenResponse.class);
                                        if (res.status == 401) {
                                            invalidAttemptFlag = true;
                                            attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                                            attentionRequiredTowardsInvalid.setText("*Invalid Enrollment/Password, Check Again");
                                            attentionRequiredTowardsInvalid.setAlpha(1);
                                            attentionRequiredTowardsPasswordTypeField.setAlpha(0);
                                            proceedingPasswordFlag = false;
                                            proceedingUsernameFlag = false;
                                        } else if (res.status == 200) {
                                            // WRITING LOGIN CREDENTIALS, ACCESS_TOKEN, REFRESH_TOKEN, ACCOUNT_TYPE IN SHARED_PREFRENCE FILE
                                            SharedPreferences sharedPref = context.getSharedPreferences( getString(R.string.user_credentials_file_key),Context.MODE_PRIVATE );
                                            SharedPreferences.Editor sharedPrefEditor = sharedPref.edit();
                                            sharedPrefEditor.putString( getString(R.string.user_id),usernameValue );
                                            sharedPrefEditor.putString( getString(R.string.password),passwordValue );
                                            sharedPrefEditor.putString( getString(R.string.account_type),getString(R.string.account_type_student) );
                                            sharedPrefEditor.putBoolean( getString(R.string.login_status),true );
                                            sharedPrefEditor.putString( getString(R.string.access_token),res.access_token );
                                            sharedPrefEditor.putString( getString(R.string.refresh_token),res.refresh_token );
                                            sharedPrefEditor.commit();

                                            attentionRequiredTowardsInvalid.setAlpha(0);
                                            startActivity(new Intent(StudentLogin.this, Dashboard.class));
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
                    }
                else {
                    loginBtn.setClickable(true);
                    if (usernameValue.equals("")) {
                        attentionRequiredTowardsUsernameField.setAlpha(1);
                        attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
                        attentionRequiredTowardsUsernameField.setText("*Required");
                        proceedingUsernameFlag = false;
                    } else {
                        attentionRequiredTowardsUsernameField.setAlpha(0);
                    }
                    if (passwordValue.equals("")) {
                        attentionRequiredTowardsPasswordTypeField.setAlpha(1);
                        attentionRequiredTowardsPasswordTypeField.setText("*Required");
                        proceedingPasswordFlag = false;
                    } else {
                        attentionRequiredTowardsPasswordTypeField.setAlpha(0);
                    }
                }
            }
        }));

    }

public static boolean isValidPassword(String password){
        if ( password.length() >= 8 ) {
            return true;
        }
        else
            return false;
    }

}