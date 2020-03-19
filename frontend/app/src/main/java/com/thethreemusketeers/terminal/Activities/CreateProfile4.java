package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import com.thethreemusketeers.terminal.R;

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
                    startActivity(new Intent(CreateProfile4.this,CreateProfile5.class));
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
