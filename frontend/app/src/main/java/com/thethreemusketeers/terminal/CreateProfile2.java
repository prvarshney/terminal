package com.thethreemusketeers.terminal;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.DialogFragment;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.text.DateFormat;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class CreateProfile2 extends AppCompatActivity implements DatePickerDialog.OnDateSetListener {

    EditText dobSelector;
    EditText username;
    TextView usernameLabel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_profile2);

        // FETCHING XML ELEMENTS
        username = findViewById(R.id.username);
        usernameLabel = findViewById(R.id.username_label);
        dobSelector = findViewById(R.id.dob_selector);

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
                if( !s.equals("") ){
                    // SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED USERNAME
                    // EXISTS OR NOT

                    Map<String, String> postParameters = new HashMap<String, String>();
                    postParameters.put("user_id",s.toString());

                    JsonObjectRequest requestObject = new JsonObjectRequest(
                            Request.Method.POST,
                            ReqURL,
                            new JSONObject(postParameters),
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    usernameLabel.setText(response.toString());
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    Log.e("Response",error.toString());
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

