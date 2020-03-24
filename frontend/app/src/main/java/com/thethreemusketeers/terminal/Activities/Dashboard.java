package com.thethreemusketeers.terminal.Activities;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.thethreemusketeers.terminal.R;

public class Dashboard extends AppCompatActivity {

    Button logout;
    Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        // FETCHING COMPONENTS FROM XML FILE
        logout = findViewById(R.id.button);

        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SharedPreferences sharedPref = context.getSharedPreferences(getString(R.string.user_credentials_file_key),Context.MODE_PRIVATE);
                SharedPreferences.Editor sharedPrefEditor = sharedPref.edit();
                sharedPrefEditor.putString( getString(R.string.user_id),"" );
                sharedPrefEditor.putString( getString(R.string.password),"" );
                sharedPrefEditor.putString( getString(R.string.account_type),"" );
                sharedPrefEditor.putBoolean( getString(R.string.login_status),false );
                sharedPrefEditor.putString( getString(R.string.access_token),"" );
                sharedPrefEditor.putString( getString(R.string.refresh_token),"" );
                sharedPrefEditor.commit();
                startActivity(new Intent(Dashboard.this,MainActivity.class));
            }
        });
    }
}
