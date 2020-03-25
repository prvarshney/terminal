package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;

import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.DatePickerFragment;
import com.thethreemusketeers.terminal.JSONRequestObject.UserRegisterObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.text.DateFormat;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class CreateProfile2 extends AppCompatActivity implements DatePickerDialog.OnDateSetListener {

    // DECLARING VARIABLES
    EditText dobSelector;
    EditText username;
    TextView attentionRequiredOnUserId;
    TextView attentionRequiredOnDOB;
    TextView usernameHeader;
    View nextBtn;
    Boolean proceedingNextFlag = false, isUserNameFieldEmpty = true, isDOBFieldEmpty = true;
    Boolean toastDisplayed = false;
    String ReqURL;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile2);

        // FETCHING XML ELEMENTS
        username = findViewById(R.id.username);
        usernameHeader = findViewById(R.id.username_header);
        attentionRequiredOnUserId = findViewById(R.id.attention_required_on_userid_editText);
        attentionRequiredOnDOB = findViewById(R.id.attention_required_on_dob);
        dobSelector = findViewById(R.id.dob_selector);
        nextBtn = findViewById(R.id.activity2_next_btn);

        // PRESENTING LAYOUT FOR USER ACCORDING TO THE ACCOUNT-TYPE HE/SHE SELECTED EARLIER
        if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_student)) ) {
            // CUSTOMIZING LAYOUT FOR STUDENT
            usernameHeader.setText("Enrollment");
            username.setHint("University Allotted Enrollment No.");
            username.setInputType(InputType.TYPE_CLASS_NUMBER);
            ReqURL = Config.HostURL + "/student/check_availability";
        }
        else if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)) ) {
            // CUSTOMIZING LAYOUT FOR FACULTY
            usernameHeader.setText("Username");
            username.setHint("Create Username, like john_doe");
            username.setInputType(InputType.TYPE_CLASS_TEXT);
            ReqURL = Config.HostURL + "/faculty/check_availability";
        }

        // SETTING DATEPICKER WITH DOB SELECTOR EDIT TEXT
        dobSelector.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DialogFragment newFragment = new DatePickerFragment();
                newFragment.show(getSupportFragmentManager(), "datePicker");
            }
        });

        // RequestQueue FOR CHECKING AVAILABILITY OF USER ENTERED STRING AS A USERNAME
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        // CHECKING FOR TEXTCHANGE ON USERNAME EDIT TEXT FIELD
        username.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if( !s.equals("") ) {
                    // SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED USERNAME
                    // EXISTS OR NOT
                    Map<String, String> postParameters = new HashMap<String, String>();
                    postParameters.put("user_id", s.toString());

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(), MessageAndStatusResponse.class);
                                    if( res.status == 206 ){
                                        attentionRequiredOnUserId.setText("(This username is unavailable)");
                                        attentionRequiredOnUserId.setAlpha(1);
                                        proceedingNextFlag = false;
                                    }
                                    else if( res.status == 200){
                                        attentionRequiredOnUserId.setAlpha(0);
                                        proceedingNextFlag = true;
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
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // CHECKING FOR TEXTCHANGE ON DOB EDIT TEXT FIELD
        dobSelector.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if ( !attentionRequiredOnDOB.getText().toString().equals("") ) {
                    attentionRequiredOnDOB.setAlpha(0);
                    isDOBFieldEmpty = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        // ADDING EVENT LISTENER ON NEXT BUTTON
        nextBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // SETTING ERROR DISPLAY TOAST FLAG TO FALSE SO THAT ONLY ONE TOAST GETS DISPLAYED
                toastDisplayed = false;
                // CHECKING WHETHER USERNAME IS NOT EMPTY
                if ( username.getText().toString().contains(" ") || username.getText().toString().equals("")) {
                    isUserNameFieldEmpty = true;
                    Toast toast = Toast.makeText(CreateProfile2.this,"",Toast.LENGTH_LONG);
                    if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)) )
                        toast.setText("Please don't use spaces in between or leave Username field empty");
                    else
                        toast.setText("Please don't use spaces in between or leave Enrollment field empty");
                    toast.setGravity(Gravity.CENTER_HORIZONTAL|Gravity.CENTER_VERTICAL,0,0);
                    toast.show();
                    toastDisplayed = true;
                }
                else
                    isUserNameFieldEmpty = false;

                // CHECKING WHETHER DATE OF BIRTH EDIT TEXT IS NOT EMPTY
                if ( dobSelector.getText().toString().equals("") ) {
                    isDOBFieldEmpty = true;
                    attentionRequiredOnDOB.setAlpha(1);
                }
                else {
                    isDOBFieldEmpty = false;
                    attentionRequiredOnDOB.setAlpha(0);
                }
                // WHEN EVERYTHING IS OKAY WE PROCEED TO NEXT ACTIVITY
                if( proceedingNextFlag && !isUserNameFieldEmpty && !isDOBFieldEmpty ) {
                    if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_faculty)) )
                        UserRegisterObject.faculty_id = username.getText().toString();
                    else if ( UserRegisterObject.account_type.equals(getString(R.string.account_type_student)) )
                        UserRegisterObject.enrollment = username.getText().toString();
                    proceedingNextFlag = false;     // SO THAT IF USER GETS BACKED FROM NEXT ACTIVITY
                                                    // IT AGAIN CHECKS FOR CHANGES
                    startActivity(new Intent(CreateProfile2.this, CreateProfile3.class));
                }

                else if ( !proceedingNextFlag && !isUserNameFieldEmpty && !isDOBFieldEmpty ) {
                    final ProgressButton progressButton = new ProgressButton(CreateProfile2.this, nextBtn);
                    progressButton.buttonProgressActivatedState("Please Wait...");
                    // SENDING USERNAME AGAIN TO THE SERVER AND CHECK FOR AVAILABILITY
                    Map<String, String> postParameters = new HashMap<String, String>();
                    postParameters.put("user_id", username.getText().toString());

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    Gson gson = new Gson();
                                    MessageAndStatusResponse res = gson.fromJson(response.toString(), MessageAndStatusResponse.class);
                                    progressButton.buttonProgressStoppedState("NEXT");
                                    if( res.status == 206 ){
                                        attentionRequiredOnUserId.setText("(This username is unavailable)");
                                        attentionRequiredOnUserId.setAlpha(1);
                                        proceedingNextFlag = false;
                                    }
                                    else if( res.status == 200){
                                        attentionRequiredOnUserId.setAlpha(0);
                                        proceedingNextFlag = false;     // SO THAT IF USER GETS BACKED FROM NEXT ACTIVITY
                                        // IT AGAIN CHECKS FOR CHANGES
                                        startActivity(new Intent(CreateProfile2.this, CreateProfile3.class));
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
                    if ( !toastDisplayed ) {
                        Toast toast = Toast.makeText(CreateProfile2.this,"Please fill all the required fields",Toast.LENGTH_SHORT);
                        toast.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL,0,0);
                        toast.show();
                        toastDisplayed = true;
                    }
                }
            }
        });
    }

    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.YEAR, year);
        calendar.set(Calendar.MONTH, month);
        calendar.set(Calendar.DAY_OF_MONTH, dayOfMonth);
        // FORMATTING DATE INTO WELL FORMATTED ZERO PRECEEDED STRUCTURE
        UserRegisterObject.dob = String.format("%02d",dayOfMonth) + "/" + String.format("%02d",month+1) + "/" + Integer.toString(year);

        // SETTING SELECTED DATE STRING TO THE EDIT TEXT
        dobSelector.setText(UserRegisterObject.dob);
    }
}

