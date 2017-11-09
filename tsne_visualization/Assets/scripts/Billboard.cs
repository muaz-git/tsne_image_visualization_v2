using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Billboard : MonoBehaviour
{

	float cameraOffestFactor = 5.0f;

	void Update()
	{

		Vector3 behindCam = Camera.main.transform.position - Camera.main.transform.forward * cameraOffestFactor;
        transform.LookAt(behindCam, Vector3.up);
	}
}

