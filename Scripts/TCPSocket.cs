using System.Collections;
using System.Collections.Generic;
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

public class TCPSocket : MonoBehaviour
{
    [SerializeField] Test2Controller controller;
    //[SerializeField] Transform target;
    // HTTP References:
    // https://gist.github.com/sdumetz/ca490544f200c7b2a92f
    // https://learn.microsoft.com/en-us/dotnet/api/system.net.httplistener
    // https://learn.microsoft.com/en-us/dotnet/api/system.net.sockets.tcplistener

    //Json References:
    //https://docs.unity3d.com/ScriptReference/JsonUtility.FromJson.html

    Thread httpListenerThread;
    //int actionID;
    //float actionValue;
    string action;

    // Start is called before the first frame update
    void Start()
    {
        //string[] prefix = new string[] { "http://127.0.0.1:8000/" };
        httpListenerThread = new Thread(new ThreadStart(Listener));
        httpListenerThread.IsBackground = true;
        httpListenerThread.Start();
    }


    // Update is called once per frame
    void Update()
    {

    }

    private void OnDestroy()
    {
        httpListenerThread.Abort();
        Debug.Log("http stop!");
    }

    void Listener()
    {
        HttpListener listener = new HttpListener();
        try
        {
            string[] prefixes = new string[] { "http://127.0.0.1:8000/" };
            // URI prefixes are required,
            // for example "http://contoso.com:8080/index/".
            if (prefixes == null || prefixes.Length == 0)
                throw new ArgumentException("prefixes");

            // Create a listener.
            
            // Add the prefixes.
            foreach (string s in prefixes)
            {
                listener.Prefixes.Add(s);
            }
            listener.Start();
            Debug.Log("Listening...");
            while (true)
            {
                string text = "test";
                // Note: The GetContext method blocks while waiting for a request.
                HttpListenerContext context = listener.GetContext();
                HttpListenerRequest request = context.Request;
                // Obtain a response object.
                HttpListenerResponse response = context.Response;

                using var reader = new StreamReader(request.InputStream);
                text = reader.ReadToEnd();
                JsonData data = JsonUtility.FromJson<JsonData>(text);
                //Debug.Log("Action ID: " + data.id + ", Action Value: " + data.value );
                //actionID = data.id;
                //actionValue = data.value;
                //controller.Action(data.id, data.value);
                action = data.action;
                controller.Action(action);


                // Construct a response.
                string responseString = "<HTML><BODY>Unity 3D Hello world!</BODY></HTML>";
                byte[] buffer = System.Text.Encoding.UTF8.GetBytes(responseString);
                // Get a response stream and write the response to it.
                response.ContentLength64 = buffer.Length;
                System.IO.Stream output = response.OutputStream;
                output.Write(buffer, 0, buffer.Length);
                // You must close the output stream.
                output.Close();
                

            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("SocketException " + socketException.ToString());
        }
        finally //For actually terminating the thread.
        {
            listener.Stop();
        }
    }


}