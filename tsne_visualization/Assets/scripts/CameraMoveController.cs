using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMoveController : MonoBehaviour {

	public float speed = 20.0f;
	public float rotSens = 100.0f;

	float minX = -360.0f;
	float maxX = 360.0f;
	float minY = -45.0f;
	float maxY = 45.0f;	

	float rotationY = 0.0f;
	float rotationX = 0.0f;

	// Use this for initialization
	void Start () {
		
	}

	void Update()
	{
		// Left Right Movement
		if (Input.GetKey(KeyCode.RightArrow))
		{
			var vec = Quaternion.Euler(0, 90, 0) * transform.forward;
			transform.position += vec * Time.deltaTime * speed;

		}
		if (Input.GetKey(KeyCode.LeftArrow))
		{
			var vec = Quaternion.Euler(0, -90, 0) * transform.forward;
			transform.position += vec * Time.deltaTime * speed;
		}
		if (Input.GetKey(KeyCode.DownArrow))
		{
			transform.position -= transform.forward * Time.deltaTime * speed;
		}
		if (Input.GetKey(KeyCode.UpArrow))
		{
			transform.position += transform.forward * Time.deltaTime * speed;
			
		}

		// Roation
		if (Input.GetMouseButton(0))
		{
			rotationX += Input.GetAxis("Mouse X") * rotSens * Time.deltaTime;
			rotationY += Input.GetAxis("Mouse Y") * rotSens * Time.deltaTime;
			rotationY = Mathf.Clamp(rotationY, minY, maxY);
			transform.localEulerAngles = new Vector3(-rotationY, rotationX, 0);
		}
	}
}
