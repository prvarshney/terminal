package com.thethreemusketeers.terminal;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.TextWatcher;
import android.text.style.ClickableSpan;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;

import com.thethreemusketeers.terminal.JSONResponseObject.MessageAndStatusResponse;

import org.json.JSONObject;

import java.text.DateFormat;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class CreateProfile2 extends AppCompatActivity implements DatePickerDialog.OnDateSetListener {

    EditText dobSelector;
    EditText username;
    TextView attentionRequiredOnUserId;
    TextView attentionRequiredOnDOB;
    Button nextBtn;
    Boolean proceedingNextFlag = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile2);

        // FETCHING XML ELEMENTS
        username = findViewById(R.id.username);
        attentionRequiredOnUserId = findViewById(R.id.attention_required_on_userid_editText);
        attentionRequiredOnDOB = findViewById(R.id.attention_required_on_dob);
        dobSelector = findViewById(R.id.dob_selector);
        nextBtn = findViewById(R.id.activity2_next_btn);

        // SETTING DATEPICKER WITH DOB SELECTOR EDIT TEXT
        dobSelector.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DialogFragment newFragment = new DatePickerFragment();
                newFragment.show(getSupportFragmentManager(), "datePicker");
            }
        });

        // CHECKING AVAILABILITY OF USER ENTERED STRING AS A USERNAME
        final String ReqURL = "https://terminal-bpit.herokuapp.com/faculty/check_availability";
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
                    proceedingNextFlag = true;
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
                // CHECKING WHETHER USERNAME IS NOT EMPTY
                if (username.getText().toString().equals("")) {
                    proceedingNextFlag = false;
                    attentionRequiredOnUserId.setText("* Required");
                    attentionRequiredOnUserId.setAlpha(1);
                }
                // CHECKING WHETHER DATE OF BIRTH EDIT TEXT IS NOT EMPTY
                if ( dobSelector.getText().toString().equals("") ) {
                    proceedingNextFlag = false;
                    attentionRequiredOnDOB.setAlpha(1);
                }
                else
                    attentionRequiredOnDOB.setAlpha(0);
                // WHEN EVERYTHING IS OKAY WE PROCEED TO NEXT ACTIVITY
                if( proceedingNextFlag )
                    startActivity(new Intent(CreateProfile2.this, CreateProfile3.class));
            }
        });
    }

    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.YEAR, year);
        calendar.set(Calendar.MONTH, month);
        calendar.set(Calendar.DAY_OF_MONTH, dayOfMonth);
        String currentDateString = DateFormat.getDateInstance(DateFormat.FULL).format(calendar.getTime());

        // SETTING SELECTED DATE STRING TO THE EDIT TEXT
        dobSelector.setText(currentDateString);
    }
}

