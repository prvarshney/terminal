package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
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

public class CreateProfile4 extends AppCompatActivity {

    Button nextBtn;
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
                if( !password.getText().toString().equals("") )
                    attentionReqOnPassword.setAlpha(0);
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
                if( !password.getText().toString().equals(confirmPassword.getText().toString()) ){
                    attentionReqOnConfirmPassword.setAlpha(1);
                    attentionReqOnConfirmPassword.setText("*Mismatch");
                }
                else {
                    attentionReqOnConfirmPassword.setAlpha(0);
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
                    passwordEye.setImageResource(R.drawable.password_eye);
                    isPasswordVisible = false;
                }
                else {
                    password.setTransformationMethod(null);
                    passwordEye.setImageResource(R.drawable.password_eye_crossed);
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
                    confirmPasswordEye.setImageResource(R.drawable.password_eye);
                }
                else {
                    confirmPassword.setTransformationMethod(null);
                    isConfirmPasswordVisible = true;
                    confirmPasswordEye.setImageResource(R.drawable.password_eye_crossed);
                }
            }
        });

        final String ReqURL = Config.HostURL + "/faculty/register";
        final RequestQueue requestQueue = Volley.newRequestQueue(this);

        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
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
                    FacultyRegisterObject.password = password.getText().toString();
                    // SENDING USER DETAILS FROM DIFFERENT ACTIVITIES TO SERVER
                    // CREATING REQUEST OBJECT
                    Map<String,String> postParameters = new HashMap<String, String>();
                    postParameters.put("name",FacultyRegisterObject.name);
                    postParameters.put("faculty_id",FacultyRegisterObject.faculty_id);
                    postParameters.put("email",FacultyRegisterObject.email);
                    postParameters.put("phone_number",FacultyRegisterObject.phone_number);
                    postParameters.put("password",FacultyRegisterObject.password);
                    postParameters.put("dob",FacultyRegisterObject.dob);

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(),MessageAndStatusResponse.class);
                                    Log.e("Response", "Hello");
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
                    requestQueue.add(requestObject);
                }
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
