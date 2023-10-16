using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlazeController : MonoBehaviour
{
    [SerializeField]
    public GameObject head;
    public GameObject shoulder_l;
    public GameObject shoulder_r;
    public GameObject elbow_l;
    public GameObject elbow_r;
    public GameObject hand_l;
    public GameObject hand_r;
    public GameObject waist_l;
    public GameObject waist_r;

    public LandmarkData landmarkData = null;

    // Start is called before the first frame update
    void Start()
    {
        head.GetComponent<Renderer>().material.color = Color.red;
        shoulder_l.GetComponent<Renderer>().material.color = Color.blue;
        elbow_l.GetComponent<Renderer>().material.color = Color.blue;
        hand_l.GetComponent<Renderer>().material.color = Color.blue;
        shoulder_r.GetComponent<Renderer>().material.color = Color.green;
        elbow_r.GetComponent<Renderer>().material.color = Color.green;
        hand_r.GetComponent<Renderer>().material.color = Color.green;
    }

    // Update is called once per frame
    void Update()
    {
        if (landmarkData != null)
        {
            Vector3 head_pos = head.transform.localPosition;
            head_pos.x = landmarkData.landmarks[0, 0] * -1;
            head_pos.y = landmarkData.landmarks[0, 1] * -1;
            head_pos.z = landmarkData.landmarks[0, 2];
            head.transform.localPosition = head_pos;

            Vector3 shoulder_l_pos = shoulder_l.transform.localPosition;
            shoulder_l_pos.x = landmarkData.landmarks[11, 0] * -1;
            shoulder_l_pos.y = landmarkData.landmarks[11, 1] * -1;
            shoulder_l_pos.z = landmarkData.landmarks[11, 2];
            shoulder_l.transform.localPosition = shoulder_l_pos;
            
            Vector3 shoulder_r_pos = shoulder_r.transform.localPosition;
            shoulder_r_pos.x = landmarkData.landmarks[12, 0] * -1;
            shoulder_r_pos.y = landmarkData.landmarks[12, 1] * -1;
            shoulder_r_pos.z = landmarkData.landmarks[12, 2];
            shoulder_r.transform.localPosition = shoulder_r_pos;

            Vector3 elbow_l_pos = elbow_l.transform.localPosition;
            elbow_l_pos.x = landmarkData.landmarks[13, 0] * -1;
            elbow_l_pos.y = landmarkData.landmarks[13, 1] * -1;
            elbow_l_pos.z = landmarkData.landmarks[13, 2];
            elbow_l.transform.localPosition = elbow_l_pos;

            Vector3 elbow_r_pos = elbow_r.transform.localPosition;
            elbow_r_pos.x = landmarkData.landmarks[14, 0] * -1;
            elbow_r_pos.y = landmarkData.landmarks[14, 1] * -1;
            elbow_r_pos.z = landmarkData.landmarks[14, 2];
            elbow_r.transform.localPosition = elbow_r_pos;

            Vector3 hand_l_pos = hand_l.transform.localPosition;
            hand_l_pos.x = landmarkData.landmarks[15, 0] * -1;
            hand_l_pos.y = landmarkData.landmarks[15, 1] * -1;
            hand_l_pos.z = landmarkData.landmarks[15, 2];
            hand_l.transform.localPosition = hand_l_pos;

            Vector3 hand_r_pos = hand_r.transform.localPosition;
            hand_r_pos.x = landmarkData.landmarks[16, 0] * -1;
            hand_r_pos.y = landmarkData.landmarks[16, 1] * -1;
            hand_r_pos.z = landmarkData.landmarks[16, 2];
            hand_r.transform.localPosition = hand_r_pos;

            Vector3 waist_l_pos = waist_l.transform.localPosition;
            waist_l_pos.x = landmarkData.landmarks[23, 0] * -1;
            waist_l_pos.y = landmarkData.landmarks[23, 1] * -1;
            waist_l_pos.z = landmarkData.landmarks[23, 2];
            waist_l.transform.localPosition = waist_l_pos;

            Vector3 waist_r_pos = waist_r.transform.localPosition;
            waist_r_pos.x = landmarkData.landmarks[24, 0] * -1;
            waist_r_pos.y = landmarkData.landmarks[24, 1] * -1;
            waist_r_pos.z = landmarkData.landmarks[24, 2];
            waist_r.transform.localPosition = waist_r_pos;
        }
    }
}
