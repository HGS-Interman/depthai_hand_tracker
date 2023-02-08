using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class HandTracking : MonoBehaviour
{
    public int hand_index = 0;
    private DepthAIHandTrackingClient htc;
    private GameObject[] landmarks;
    public GameObject landmarkPrefab;
    public Vector3 landmarks_scale = new Vector3(-50, -50, 50);
    public Vector3 xyz_scale = new Vector3(0.05f, 0.05f, 0.05f);

    private bool running = true;

    // Start is called before the first frame update
    void Start()
    {
        htc = new DepthAIHandTrackingClient();
        landmarks = new GameObject[21];
        for(int i=0; i < 21; i++)
        {
            landmarks[i] = Instantiate(landmarkPrefab, new Vector3(0,0,0), Quaternion.identity);
            landmarks[i].transform.parent = this.transform;
        }
        StartCoroutine("trackingLoop");
    }

    IEnumerator trackingLoop()
    {
        while(running){
            var hti = htc.getHandTrackingInfo();
            if(hti != null && hti.hands != null && hti.hands.Length > hand_index)
            {
                var hand = hti.hands[hand_index];
                this.transform.position = Vector3.Scale(hand.xyz, new Vector3(-0.05f,0.05f,0.05f));
                for(int i=0; i < 21; i++)
                {
                    landmarks[i].transform.localPosition = Vector3.Scale(hand.rotated_world_landmarks[i], landmarks_scale);
                }
            }
            else
            {
                for(int i=0; i < 21; i++)
                {
                    landmarks[i].transform.localPosition = new Vector3(0,0,0);
                }
            }
            yield return new WaitForSeconds(0.01f);
        }
        yield break;
    }

    // Update is called once per frame
    void Update()
    {
    }

    void OnDestroy()
    {
        running = false;
    }
}
