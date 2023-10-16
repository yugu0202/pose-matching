using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UnitychanIK : MonoBehaviour {
    public Transform shoulder_l;
    public Transform shoulder_r;
    public Transform elbow_l;
    public Transform elbow_r;
    public Transform hand_l;
    public Transform hand_r;
    public Transform waist_l;
    public Transform waist_r;

    public bool start = false;

    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void OnAnimatorIK()
    {
        if (!start) return;

        //左腕のIK
        animator.SetIKPositionWeight(AvatarIKGoal.LeftHand, 1);
        animator.SetIKRotationWeight(AvatarIKGoal.LeftHand, 1);

        animator.SetIKPosition(AvatarIKGoal.LeftHand, hand_l.position);
        animator.SetIKRotation(AvatarIKGoal.LeftHand, hand_l.rotation);

        animator.SetIKHintPositionWeight(AvatarIKHint.LeftElbow, 1);

        animator.SetIKHintPosition(AvatarIKHint.LeftElbow, elbow_l.position);

        //右腕のIK
        animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1);
        animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1);

        animator.SetIKPosition(AvatarIKGoal.RightHand, hand_r.position);
        animator.SetIKRotation(AvatarIKGoal.RightHand, hand_r.rotation);

        animator.SetIKHintPositionWeight(AvatarIKHint.RightElbow, 1);

        animator.SetIKHintPosition(AvatarIKHint.RightElbow, elbow_r.position);

        //腰の位置
        Vector3 waist_l_pos = waist_l.position;
        Vector3 waist_r_pos = waist_r.position;
        Vector3 waist;

        waist.x = (waist_l_pos.x + waist_r_pos.x) / 2;
        waist.y = (waist_l_pos.y + waist_r_pos.y) / 2;
        waist.z = (waist_l_pos.z + waist_r_pos.z) / 2;

        animator.bodyPosition = waist;
    }
}