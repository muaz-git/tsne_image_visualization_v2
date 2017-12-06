﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Billboard : MonoBehaviour
{

	float cameraOffestFactor = 5.0f;

	void Update()
	{
		lookAwayFromCam();
    }

	private void lookCamDirection()
	{
		// all images have same angle
		Vector3 camFaceDirection = transform.position + Camera.main.transform.rotation * Vector3.forward;
		transform.LookAt(camFaceDirection, Vector3.up);
	}

	public void lookAwayFromCam()
	{
		//all images look at a point behind the camera
		Vector3 behindCam = Camera.main.transform.position - Camera.main.transform.forward * cameraOffestFactor;
		Vector3 fromCam = -1 * (behindCam - transform.position).normalized;
		transform.forward = fromCam;
	}
}

