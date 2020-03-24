package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
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
import com.thethreemusketeers.terminal.JSONRequestObject.StudentForgotPasswordObject;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusEmailResponse;
import com.thethreemusketeers.terminal.ProgressButton;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

public class StudentRecoverPassword1<val> extends AppCompatActivity {

    EditText username;
    TextView attentionRequiredTowardsUsernameField, attentionRequiredTowardsInvalid;
    View nextBtn;
    Boolean isUsernameEmptyFlag = false, invalidAttemptFlag= false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_recover_password1);

        //Fetching XML Elements
        username = findViewById(R.id.username);
        nextBtn = findViewById(R.id.next_btn);
        attentionRequiredTowardsUsernameField = findViewById(R.id.attention_required_on_username_editText);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_on_username_editText);

        //CHECK THE CREDENTIALS ENTERED BY THE USER
        final RequestQueue requestQueue = Volley.newRequestQueue(this);

        // ADDING TEXT WATCHER ON USERNAME FIELD

        username.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(isUsernameEmptyFlag){
                    attentionRequiredTowardsUsernameField.setAlpha(0);
                    isUsernameEmptyFlag = false;
                }
                if(invalidAttemptFlag){
                    attentionRequiredTowardsInvalid.setAlpha(0);
                    invalidAttemptFlag = false;
                }
            }
            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        // CLICK EVENT LISTENER
        nextBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
             nextBtn.setClickable(false);
             final String usernameValue = username.getText().toString();
            if(!usernameValue.equals("")){
                final ProgressButton progressButton = new ProgressButton(StudentRecoverPassword1.this, nextBtn);
                progressButton.buttonProgressActivatedState("Please Wait...");
                //SENDING POST REQ TO THE SERVER TO CHECK WHETHER USER SELECTED PASSWORD
            // EXISTS OR NOT
            final String ReqURL = Config.HostURL + "/student/forgot_password/" + usernameValue;
            JsonObjectRequest requestObject = new JsonObjectRequest(
                    Request.Method.GET,
                    ReqURL,
                    null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Gson gson = new Gson();
                            nextBtn.setClickable(true);
                            progressButton.buttonProgressStoppedState("NEXT");
                            MessageStatusEmailResponse res = gson.fromJson(response.toString(), MessageStatusEmailResponse.class);
                            if (res.status == 200) {
                                attentionRequiredTowardsInvalid.setAlpha(0);
                                invalidAttemptFlag = false;
                                StudentForgotPasswordObject.userid = usernameValue;
                                startActivity(new Intent(StudentRecoverPassword1.this, StudentRecoverPassword2.class));
                            } else if(res.status == 206){
                                invalidAttemptFlag = true;
                                attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
                                attentionRequiredTowardsInvalid.setText("*Invalid Enrollment.");
                                attentionRequiredTowardsInvalid.setAlpha(1);
                            }
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Log.e("Response",error.toString());
                        }
                    }
            );
                requestObject.setRetryPolicy(new DefaultRetryPolicy(20000,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
                requestQueue.add(requestObject);
        }
        else {
            nextBtn.setClickable(true);
            if (usernameValue.equals("")) {
                attentionRequiredTowardsUsernameField.setAlpha(1);
                attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_START);
                attentionRequiredTowardsUsernameField.setText("*Required");
                attentionRequiredTowardsUsernameField.setTextAlignment(View.TEXT_ALIGNMENT_TEXT_END);
                isUsernameEmptyFlag = true;
            } else {
                attentionRequiredTowardsUsernameField.setAlpha(0);
            }
        }
    }
    }));
    }
}
