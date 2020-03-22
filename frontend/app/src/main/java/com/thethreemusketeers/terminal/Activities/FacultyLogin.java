package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.TextWatcher;
import android.text.style.ClickableSpan;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.thethreemusketeers.terminal.JSONResponseObject.MessageStatusTokenResponse;
import com.thethreemusketeers.terminal.R;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class FacultyLogin extends AppCompatActivity {

    Spinner accountTypeDropdown;
    TextView forgotPasswordLink , signUpLink;
    EditText facultyId , facultyPassword;
    Button loginBtn;
    TextView attentionRequiredTowardsFacultyId , attentionRequiredTowardsFacultyPassword, attentionRequiredTowardsInvalid;
    Boolean proceedingNextFlagId = true;
    Boolean proceedingNextFlagPassword = true;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_faculty_login);
        accountTypeDropdown = findViewById(R.id.accountType_dropdown);
        forgotPasswordLink = findViewById(R.id.forgot_password);
        signUpLink = findViewById(R.id.sign_up);
        facultyId = findViewById(R.id.facultyId);
        facultyPassword = findViewById(R.id.facultyPassword);
        loginBtn = findViewById(R.id.login_btn);
        attentionRequiredTowardsFacultyId = findViewById(R.id.attention_required_on_facultyId);
        attentionRequiredTowardsFacultyPassword = findViewById(R.id.attention_required_on_facultyPassword);
        attentionRequiredTowardsInvalid = findViewById(R.id.attention_required_on_username_editText);

        //SETTING DROPDOWN ELEMENTS
        String[] accountTypeDropdownElements = new String[]{"Change Account Type","Student"};
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
                        startActivity(new Intent(FacultyLogin.this, StudentLogin.class));
                        break;
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> arg0)
            {

            }
        });


        SpannableString forgottenPassword = new SpannableString("Forgotten your details? Get help with signing in.");
        SpannableString signUp = new SpannableString("Don't have an account? Sign Up");
        ClickableSpan forgottenPasswordActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                //launch new activity
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds){
                ds.setUnderlineText(false);
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setFakeBoldText(true);
            }
        };

        ClickableSpan signUpActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                //launch new activity
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds){
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(true);
            }
        };

        forgottenPassword.setSpan(forgottenPasswordActivityLauncher, 24, 49, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        signUp.setSpan(signUpActivityLauncher, 23, 30,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        forgotPasswordLink.setText(forgottenPassword);
        signUpLink.setText(signUp);

        final String FacReqURL = "https://terminal-bpit.herokuapp.com/faculty/login";
        final RequestQueue requestQueue = Volley.newRequestQueue(this);

        //CHECKING FOR TEXTCHANGE ON USERNAME EDIT TEXT FIELD
        facultyId.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(!s.equals("")){
                    attentionRequiredTowardsFacultyId.setAlpha(0);
                }

            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

        facultyPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(!s.equals("")){
                    attentionRequiredTowardsFacultyPassword.setAlpha(0);
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });

//        loginBtn.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                //CHECKING WHETHER ALL THE FIELDS ARE FILLED WITH USERDATA OR NOT
//                String idValue = facultyId.getText().toString();
//                String passwordValue = facultyPassword.getText().toString();
//                Boolean proceedingNextFlagId = true;
//                Boolean proceedingNextFlagPassword = true;
//                if(idValue.equals("")){
//                    attentionRequiredTowardsFacultyId.setAlpha(1);
//                    proceedingNextFlagId = false;
//                }
//                else{
//                    attentionRequiredTowardsFacultyId.setAlpha(0);
//                }
//                if(passwordValue.equals("")){
//                    attentionRequiredTowardsFacultyPassword.setAlpha(1);
//                    proceedingNextFlagPassword = false;
//                }
//                else
//                    attentionRequiredTowardsFacultyPassword.setAlpha(0);
//
//                if(proceedingNextFlagId){
//                    if(proceedingNextFlagPassword){
//                        startActivity(new Intent(FacultyLogin.this, CreateProfile2.class));
//                    }
//                    else{
//                        startActivity(new Intent(FacultyLogin.this, MainActivity.class));
//                    }
//                }
//            }
//        });

        //CHECK THE CREDENTIALS ENTERED BY USER
        final String ReqfacURL = "https://terminal-bpit.herokuapp.com/faculty/login";
        final RequestQueue requestQueue1 = Volley.newRequestQueue(this);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
               String facultyIdValue = facultyId.getText().toString();
               String facultyPasswordValue = facultyPassword.getText().toString();

               if(!facultyIdValue.equals("") && (!facultyPasswordValue.equals(""))){
                   //SENDING POST REQUEST TO THE SERVER TO CHECK WHETHER THE USER EXISTS OR NOT
                   Map<String, String> postParameters = new HashMap<String, String>();
                   postParameters.put("faculty_id",facultyIdValue);
                   postParameters.put("password",facultyPasswordValue);

                   JsonObjectRequest requestObjectfac = new JsonObjectRequest(
                           Request.Method.POST,
                           ReqfacURL,
                           new JSONObject(postParameters),
                           new Response.Listener<JSONObject>() {
                               @Override
                               public void onResponse(JSONObject response) {
                                   Gson gson = new Gson();
                                   MessageStatusTokenResponse res = gson.fromJson(response.toString(), MessageStatusTokenResponse.class);
                                   if (res.status == 401) {
                                       attentionRequiredTowardsInvalid.setText("Invalid Id or Password");
                                       attentionRequiredTowardsInvalid.setAlpha(1);
                                       proceedingNextFlagId = false;
                                       proceedingNextFlagPassword = false;

                                   } else if (res.status == 200) {
                                       attentionRequiredTowardsInvalid.setAlpha(0);
                                       startActivity(new Intent(FacultyLogin.this, MainActivity.class));

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
                   requestQueue1.add(requestObjectfac);
               }
               else{
                   if(facultyIdValue.equals("")){
                       attentionRequiredTowardsFacultyId.setAlpha(1);
                       proceedingNextFlagId = false;
                   }
                   else{
                       attentionRequiredTowardsFacultyId.setAlpha(0);
                   }
                   if(facultyPasswordValue.equals("")){
                       attentionRequiredTowardsFacultyPassword.setAlpha(1);
                       proceedingNextFlagPassword = false;
                   }
                   else
                       attentionRequiredTowardsFacultyPassword.setAlpha(0);


               }
            }
        });


    }


}
