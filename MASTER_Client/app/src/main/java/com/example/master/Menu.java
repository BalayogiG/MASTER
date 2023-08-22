package com.example.master;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

public class Menu extends AppCompatActivity {

    Button btnregister, btnlogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        btnregister = findViewById(R.id.btnregister);
        btnlogin = findViewById(R.id.btnlogin);

        btnregister.setOnClickListener(view -> {
            Intent intent = getIntent();
            String url = intent.getStringExtra("url");
            String reg_url = url + "/confirmRegistration";
            Intent intent1 = new Intent(Menu.this, RegisterAssist.class);
            intent1.putExtra("url",reg_url);
            startActivity(intent1);
        });

        btnlogin.setOnClickListener(view -> {
            Intent intent = getIntent();
            String url = intent.getStringExtra("url");
            String log_url = url + "/Login";
            Intent intent2 = new Intent(Menu.this, Login.class);
            intent2.putExtra("url",log_url);
            startActivity(intent2);
        });
    }
}