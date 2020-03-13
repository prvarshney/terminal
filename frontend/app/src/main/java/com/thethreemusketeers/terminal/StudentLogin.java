package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusTokenResponse;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class StudentLogin extends AppCompatActivity {

    Spinner accountTypeDropdown;
    EditText passwordEditText, userId ;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsPasswordTypeField,attentionRequiredTowardsInvalid;
    ImageView passwordEye;
    Boolean eyeTogglerFlag = true, proceedingUsernameFlag=false, proceedingPasswordFlag=false;
    Button loginBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login);

        //Fetching XML Elements
        accountTypeDropdown = findViewById(R.id.account_type_dropdown);
        passwordEditText = findViewById(R.id.password_edit_text);
        passwordEye = findViewById(R.id.password_eye);
        userId = findViewById(R.id.userid);
        loginBtn = findViewById(R.id.login_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsPasswordTypeField = findViewById(R.id.attention_required_on_password_editText);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_for_invalid);

        //SETTING DROPDOWN ELEMENTS
        String[] accountTypeDropdownElements = new String[]{"Student ( Change Account-Type)","Faculty"};
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
                        startActivity(new Intent(StudentLogin.this, MainActivity.class));
                        break;
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {

            }
        });

        //CHECK THE CREDENTAILS ENTERED BY THE USER.
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = "https://terminal-bpit.herokuapp.com/student/login";

        //setting event listeners
        passwordEye.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if(eyeTogglerFlag){
                    passwordEditText.setTransformationMethod(null);
                    eyeTogglerFlag = false;
                    passwordEye.setImageResource(R.drawable.password_eye_crossed);
                } else{
                    passwordEditText.setTransformationMethod(new PasswordTransformationMethod());
                    eyeTogglerFlag = true;
                    passwordEye.setImageResource(R.drawable.password_eye);
                }
            }
        })
        );

        //setting event listeners
        loginBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                 String usernameValue = userId.getText().toString();
                 String passwordValue = passwordEditText.getText().toString();

                if(!passwordValue.equals("") && (!usernameValue.equals(""))){
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
                                        MessageStatusTokenResponse res = gson.fromJson(response.toString(), MessageStatusTokenResponse.class);
                                        if (res.status == 401) {
                                            attentionRequiredTowardsInvalid.setText("Invalid User Id/Password");
                                            attentionRequiredTowardsInvalid.setAlpha(1);
                                            proceedingPasswordFlag = false;
                                            proceedingUsernameFlag = false;
                                        } else if (res.status == 200) {
                                            attentionRequiredTowardsInvalid.setAlpha(0);
                                            startActivity(new Intent(StudentLogin.this, MainActivity.class));

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
                else {
                    if (usernameValue.equals("")) {
                        attentionRequiredTowardsUsernameField.setAlpha(1);
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
}
