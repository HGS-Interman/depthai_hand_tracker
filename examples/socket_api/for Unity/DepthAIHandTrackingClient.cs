using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;

[Serializable]
public class HandTrackingInfo
{
    public Hand[] hands;
}


[Serializable]
public class Hand
{
    public string gesture;
    public float handedness;
    public int index_state;
    public string label;
    public Vector2[] landmarks;
    public int little_state;
    public float lm_score;
    public int middle_state;
    public Vector3[] norm_landmarks;
    public float rect_h_a;
    public Vector2[] rect_points;
    public float rect_w_a;
    public float rect_x_center_a;
    public float rect_y_center_a;
    public int ring_state;
    public float rotation;
    public Vector3[] rotated_world_landmarks;
    public float thumb_angle;
    public int thumb_state;
    public Vector3[] world_landmarks;
    public Vector3 xyz;
    public Vector3 xyz_zone;

    public override string ToString()
    {
        return string.Format("[{0}, {1}]", gesture, xyz);
    }
}
public class DepthAIHandTrackingClient
{
    public string m_ipAddress = "127.0.0.1";
    public int    m_port      = 7010;

    private TcpClient     m_tcpClient;
    private NetworkStream m_networkStream;

    public DepthAIHandTrackingClient()
    {

    }

    public HandTrackingInfo getHandTrackingInfo()
    {
        try
        {
            m_tcpClient = new TcpClient(m_ipAddress, m_port);
            m_networkStream = m_tcpClient.GetStream();
            // Debug.LogFormat( "接続成功" );
            var buffer = new byte[204800];
            var count = m_networkStream.Read(buffer, 0, buffer.Length);
            var message = Encoding.UTF8.GetString( buffer, 0, count );
            var handTrackingInfo = JsonUtility.FromJson<HandTrackingInfo>(message);
            return handTrackingInfo;
        }
        catch( SocketException)
        {
            Debug.LogError("接続失敗");
        }
        catch
        {
            Debug.LogError("不明なエラー");
        }
        return new HandTrackingInfo();
    }
}
