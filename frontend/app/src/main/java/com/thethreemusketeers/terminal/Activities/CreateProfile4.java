package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
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
import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class CreateProfile4 extends AppCompatActivity {

    // DECLARING VARIABLES
    View nextBtn;
    EditText password, confirmPassword;
    TextView attentionReqOnPassword, attentionReqOnConfirmPassword;
    ImageView passwordEye, confirmPasswordEye;
    boolean isPasswordVisible = false, isConfirmPasswordVisible = false, isPasswordEmpty = true, isConfirmPasswordEmpty = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile4);

        // FETCHING ELEMENTS FROM LAYOUT DESIGN
        nextBtn = findViewById(R.id.activity4_next_btn);
        password = findViewById(R.id.registration_password_editText);
        confirmPassword = findViewById(R.id.registration_confirm_password_editText);
        attentionReqOnPassword = findViewById(R.id.attention_required_on_password_editText);
        attentionReqOnConfirmPassword = findViewById(R.id.attention_required_on_confirm_password_editText);
        passwordEye = findViewById(R.id.password_eye);
        confirmPasswordEye = findViewById(R.id.confirm_password_eye);

        // ADDING TEXT WATCHER ON PASSWORD FIELDS
        password.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // DISABLING ATTENTION REQUIRED FIELD WHEN FIELD IS COMPLETE EMPTY
                if( s.toString().equals("") )
                    attentionReqOnPassword.setAlpha(0);

                // CHECKING THE VALUE OF FIELD PASSWORD WITH CONFIRM PASSWORD FIELD LIVELY
                // ONLY WHEN CONFIRM PASSWORD FIELD ISN'T EMPTY
                else if ( !confirmPassword.getText().toString().equals("") ) {
                    // RUNS WHEN USER FILED CONFIRM PASSWORD FIELD FIRST AND THEN FILLING
                    // PASSWORD FIELD
                    if ( !s.toString().equals(confirmPassword.getText().toString()) ) {
                        attentionReqOnPassword.setText("*Mismatch");
                        attentionReqOnPassword.setAlpha(1);
                    }
                    // DISABLING WARNING FROM BOTH FIELDS IF BOTH ARE EQUAL
                    else if ( confirmPassword.getText().toString().equals(s.toString()) ) {
                        attentionReqOnConfirmPassword.setAlpha(0);
                        attentionReqOnPassword.setAlpha(0);
                    }
                }
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        confirmPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                // DISABLING ATTENTION REQUIRED FIELD WHEN FIELD IS COMPLETE EMPTY
                if( s.toString().equals("") )
                    attentionReqOnPassword.setAlpha(0);

                // RUNS WHEN PASSWORD FILED ISN'T EMPTY AND PASSWORD FIELD AND CONFIRM PASSWORD FIELD
                // BOTH HAVE DIFFERENT VALUES
                else if( !password.getText().toString().equals("") && !password.getText().toString().equals(s.toString()) ){
                    attentionReqOnConfirmPassword.setAlpha(1);
                    attentionReqOnConfirmPassword.setText("*Mismatch");
                }
                // DISABLING WARNING FROM BOTH FIELDS IF BOTH ARE EQUAL
                else if ( password.getText().toString().equals(s.toString()) ) {
                    attentionReqOnConfirmPassword.setAlpha(0);
                    attentionReqOnPassword.setAlpha(0);
                }
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // CREATING EVENT LISTENERS
        passwordEye.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isPasswordVisible) {
                    password.setTransformationMethod(new PasswordTransformationMethod());
                    passwordEye.setImageResource(R.drawable.ic_password_eye_image);
                    isPasswordVisible = false;
                }
                else {
                    password.setTransformationMethod(null);
                    passwordEye.setImageResource(R.drawable.ic_password_eye_crossed_image);
                    isPasswordVisible = true;
                }
            }
        });

        confirmPasswordEye.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConfirmPasswordVisible) {
                    confirmPassword.setTransformationMethod(new PasswordTransformationMethod());
                    isConfirmPasswordVisible = false;
                    confirmPasswordEye.setImageResource(R.drawable.ic_password_eye_image);
                }
                else {
                    confirmPassword.setTransformationMethod(null);
                    isConfirmPasswordVisible = true;
                    confirmPasswordEye.setImageResource(R.drawable.ic_password_eye_crossed_image);
                }
            }
        });

        // PREPARING TO SEND USER ENTERED DETAILS TO SERVER WITH DIFFERENT ROUTES BASED ON ACCOUNT
        // TYPE USER SELECTED
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty))
                    ? Config.HostURL + "/faculty/register"
                    : Config.HostURL + "/student/register" ;

        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nextBtn.setClickable(false);
                if ( password.getText().toString().equals("") ) {
                    attentionReqOnPassword.setText("*Required");
                    attentionReqOnPassword.setAlpha(1);
                    isPasswordEmpty = true;
                }
                else
                    isPasswordEmpty = false;

                if ( confirmPassword.getText().toString().equals("") ) {
                    attentionReqOnConfirmPassword.setText("*Required");
                    attentionReqOnConfirmPassword.setAlpha(1);
                    isConfirmPasswordEmpty = true;
                }
                else
                    isConfirmPasswordEmpty = false;

                if( password.getText().toString().equals(confirmPassword.getText().toString()) && !isPasswordEmpty && !isConfirmPasswordEmpty ) {
                    UserRegisterObject.password = password.getText().toString();
                    final ProgressButton progressButton = new ProgressButton(CreateProfile4.this,nextBtn);
                    progressButton.buttonProgressActivatedState("Please Wait...");
                    // SENDING USER DETAILS FROM DIFFERENT ACTIVITIES TO SERVER
                    // CREATING REQUEST OBJECT
                    Map<String,String> postParameters = new HashMap<String, String>();
                    postParameters.put("name",UserRegisterObject.name);
                    postParameters.put("faculty_id",UserRegisterObject.faculty_id);
                    postParameters.put("ic_sent_mail_image",UserRegisterObject.email);
                    postParameters.put("phone_number",UserRegisterObject.phone_number);
                    postParameters.put("password",UserRegisterObject.password);
                    postParameters.put("dob",UserRegisterObject.dob);

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    nextBtn.setClickable(true);
                                    progressButton.buttonProgressStoppedState("NEXT");
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(),MessageAndStatusResponse.class);
                                    if ( res.status == 200 )
                                        startActivity(new Intent(CreateProfile4.this,CreateProfile5.class));
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
                else
                    nextBtn.setClickable(true);
            }
        });
    }

    public static boolean isValidPassword(String password){
        if ( password.length() >= 8 ) {
            return true;
        }
        else
            return false;
    }

}
