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
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.Config;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusEmailResponse;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

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

        nextBtn.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String usernameValue = username.getText().toString();

                if(!usernameValue.equals("")){
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
                                    MessageStatusEmailResponse res = gson.fromJson(response.toString(), MessageStatusEmailResponse.class);
                                    if (res.status == 206) {
//                                        invalidAttemptFlag = true;
                                        attentionRequiredTowardsInvalid.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
                                        attentionRequiredTowardsInvalid.setText("*Invalid Enrollment, Check Again");
                                        attentionRequiredTowardsInvalid.setAlpha(1);
//                                        proceedingFlag = false;
                                    } else if (res.status == 200) {
                                        attentionRequiredTowardsInvalid.setAlpha(0);
                                        startActivity(new Intent(StudentRecoverPassword.this, CreateProfile1.class));
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
                    requestQueue.add(requestObject);

                } else {

                    if (usernameValue.equals("")) {
                        attentionRequiredTowardsUsernameField.setAlpha(1);
                        attentionRequiredTowardsUsernameField.setText("*Required");
//                        proceedingFlag = false;
                    } else {
                        attentionRequiredTowardsUsernameField.setAlpha(0);
//                        proceedingFlag = true;
                    }
                }
            }
        }));
    }
}
