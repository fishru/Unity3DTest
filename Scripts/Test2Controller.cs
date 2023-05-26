using StarterAssets;
using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class Test2Controller : MonoBehaviour
{
    [SerializeField] StarterAssetsInputs inputs;
    [SerializeField] Vector2 direction;
    [SerializeField] float jumpState;
    [SerializeField] float sprintState;
    int hMove = 100;
    int vMove = 101;
    int jump = 102;
    int sprint = 103;
    float hInput;
    float vInput;
    float waitTime = 0.5f;
    float timer = 0.0f;
    int actionID;
    float actionValue;

    Dictionary<string, Action> actionCategory;
    Dictionary<int, Action<float>> actionList;
    // Start is called before the first frame update
    void Start()
    {
        actionCategory = new()
        {
            { "Left", () => { actionID = hMove; actionValue = -1; } },
            { "Right", () => { actionID = hMove; actionValue = 1; } },
            { "Forward", () => { actionID = vMove; actionValue = 1; } },
            { "Back", () => { actionID = vMove; actionValue = -1; } },
            { "Jump", () => { actionID = jump; actionValue = 1; } }
        };
        actionList = new()
        {
            { hMove, x => { timer = 0.0f; hInput = x; vInput = 0; } },
            { vMove, x => { timer = 0.0f; vInput = x; hInput = 0; } },
            { jump, x => jumpState = x },
            { sprint, x => sprintState = x }
        };
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= waitTime)
        {
            hInput = 0;
            vInput = 0;
            timer = 0.0f;
        }

        direction.x = hInput;
        direction.y = vInput;
        inputs.MoveInput(direction);
        jumpCheck();
        sprintCheck();
    }

    private void jumpCheck()
    {
        if (jumpState > 0)
        {
            inputs.JumpInput(Convert.ToBoolean(jumpState));
        }
        jumpState = 0;
    }

    private void sprintCheck()
    {
        inputs.SprintInput(Convert.ToBoolean(sprintState));
    }

    //public void Action(int actionID, float actionValue)
    public void Action(string action)
    {

        //Debug.Log("actionID: " + actionID + ", actionValue: " + actionValue);
        Debug.Log("Action: " + action);
        actionCategory[action].DynamicInvoke();
        actionList[actionID].DynamicInvoke(actionValue);
    }
}
