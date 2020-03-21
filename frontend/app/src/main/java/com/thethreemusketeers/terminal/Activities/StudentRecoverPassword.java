package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusEmailResponse;
import com.thethreemusketeers.terminal.R;

public class StudentRecoverPassword<val> extends AppCompatActivity {

    EditText username;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsInvalid;
    Button nextBtn;
    Boolean proceedingFlag = false, invalidAttemptFlag= false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_recover_password);

        //Fetching XML Elements
        username = findViewById(R.id.username);
        nextBtn = findViewById(R.id.next_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_on_username_editText);

        //CHECK THE CREDENTIALS ENTERED BY THE USER
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = Config.HostURL + "/student/forgot_password/<user_id>";


    }
}
