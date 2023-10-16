using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Newtonsoft.Json;
using UnityEngine;

public class LandmarkData
{
    public bool ok { get; set; }
    public float[,] landmarks { get; set; }
}

public class PythonNetwork : SingletonMonoBehaviour<PythonNetwork>
{
    public BlazeController blazeCon;

    static UdpClient udp;
    Thread receiveThread;

    // Start is called before the first frame update
    void Start()
    {
        int LOCAL_PORT = 53000;
        
        udp = new UdpClient(LOCAL_PORT);

        receiveThread = new Thread(new ThreadStart(ThreadReaceive));
        receiveThread.Start();
    }

    // Update is called once per frame
    void Update()
    {
    }

    void ThreadReaceive()
    {
        while (true)
        {
            IPEndPoint remoteEP = null;
            byte[] data = udp.Receive(ref remoteEP);
            Parse(remoteEP, data);
        }
    }

    void Parse(IPEndPoint remoteEP, byte[] data)
    {
        string text = Encoding.UTF8.GetString(data);
        LandmarkData landmarkData = JsonConvert.DeserializeObject<LandmarkData>(text);
        if (landmarkData.ok)
        {
            blazeCon.landmarkData = landmarkData;
        }
    }
}
