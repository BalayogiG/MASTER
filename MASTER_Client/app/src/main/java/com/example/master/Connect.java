package com.example.master;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Connect extends AppCompatActivity {

    EditText ip_address, port_num;
    Button btnConnect;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect);

        ip_address = findViewById(R.id.ip_address);
        port_num = findViewById(R.id.port_num);

        btnConnect = findViewById(R.id.btnConnect);

        btnConnect.setOnClickListener(view -> {
            String ip = ip_address.getText().toString();
            String port = port_num.getText().toString();
            InputValidator(ip, port);
            String url = UrlFormer(ip, port);
            Intent intent = new Intent(Connect.this, Menu.class);
            intent.putExtra("url", url);
            startActivity(intent);
        });
    }

    private String UrlFormer(String ip, String port) {
        String url = "http://"+ip+":"+port;
        return url;
    }

    private void InputValidator(String ip, String port) {
        if (ip.contentEquals("")){
            Toast.makeText(this, "Kindly Enter IP address", Toast.LENGTH_SHORT).show();
        }
        if (port.contentEquals("")){
            Toast.makeText(this, "Kindly Enter Port Number", Toast.LENGTH_SHORT).show();
        }
        if (ip.contentEquals("") && port.contentEquals("")){
            Toast.makeText(this, "Kindly Enter IP address and Port number", Toast.LENGTH_SHORT).show();
        }
    }
}