package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.R;

public class StudentRecoverPassword extends AppCompatActivity {

    EditText username;
    TextView attentionRequiredTowardsUsernameField;
    Button loginBtn;
    Boolean proceedingFlag = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_recover_password);

        //Fetching XML Elements
        username = findViewById(R.id.username);
        loginBtn = findViewById(R.id.login_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);

        //CHECK THE CREDENTIALS ENTERED BY THE USER
        final RequestQueue requestQueue = Volley.newRequestQueue(this);
        final String ReqURL = Config.HostURL + "/student/forgot_password/<user_id>";

        loginBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String usernameValue = username.getText().toString();

                if(usernameValue.equals("")){
                    attentionRequiredTowardsUsernameField.setAlpha(1);
                    proceedingFlag = false;
                } else {
                    attentionRequiredTowardsUsernameField.setAlpha(0);
                    proceedingFlag = true;
                }
                if(proceedingFlag){
                    startActivity(new Intent(StudentRecoverPassword.this, MainActivity.class));
                }
            }
        }));
    }
}
