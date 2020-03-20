package com.thethreemusketeers.terminal.Activities;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextPaint;
import android.text.method.LinkMovementMethod;
import android.text.style.ClickableSpan;
import android.text.style.StyleSpan;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.thethreemusketeers.terminal.R;
import com.thethreemusketeers.terminal.TermsAndConditionActivity;

public class MainActivity extends AppCompatActivity {

    TextView termsAndConditionLink;
    Button agreeAndContinueBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // GETTING COMPONENTS FROM LAYOUT
        termsAndConditionLink = findViewById(R.id.tc_link);
        agreeAndContinueBtn = findViewById(R.id.agree_btn);

        // CREATING TERMSANDCONDITION LINK CLICKABLE
        SpannableString termsAndCondition = new SpannableString("Tap \"Agree and Continue\" to accept the Terms of Service and Privacy Policy.\nAlready Signup? Login");
        ClickableSpan termsAndConditionActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                startActivity(new Intent(MainActivity.this, TermsAndConditionActivity.class));
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setUnderlineText(false);
                ds.setColor( getResources().getColor(R.color.colorMatteGreen));
                ds.setTypeface(Typeface.DEFAULT_BOLD);
            }
        };
        ClickableSpan loginActivityLauncher = new ClickableSpan() {
            @Override
            public void onClick(@NonNull View widget) {
                // LAUNCH LOGIN ACTIVITY
                startActivity(new Intent(MainActivity.this, StudentLogin.class));
            }

            @Override
            public void updateDrawState(@NonNull TextPaint ds) {
                ds.setColor(getResources().getColor(R.color.colorMatteGreen));
                ds.setUnderlineText(false);
                ds.setTypeface(Typeface.DEFAULT_BOLD);
            }
        };
        termsAndCondition.setSpan(termsAndConditionActivityLauncher,39,55, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        termsAndCondition.setSpan(loginActivityLauncher,92,97,Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);

        termsAndConditionLink.setText(termsAndCondition);
        termsAndConditionLink.setMovementMethod(LinkMovementMethod.getInstance());

        // SETTING EVENT LISTENER ON CLICK BUTTON
        agreeAndContinueBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                startActivity(new Intent(MainActivity.this,CreateProfile1.class));
                startActivity(new Intent( MainActivity.this, FacultyLogin.class));
            }
        });
    }
}
