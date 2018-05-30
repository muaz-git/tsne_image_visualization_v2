using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON;
using System.IO;

// room position: x, y, z = -1.5, 0, 0
// room scale: x, y, z = 0.1, 0.6, 0.126
// OVR position: x, y, z = 0, 2, 1.33
// OVR Scale: 1, 1, 1
// x distance calculated = 3.072
// y distance calculated = 3.57
// z distance calculated = 3.82


public class ImageManager : MonoBehaviour
{
	

	public float scaleFactor = 0.2f;

	public bool busy = false;

	public string jsonFile = @"C:\Users\IML\tsne_image_visualization\backend\data.json";
	public string imageFolder = @"C:\Users\IML\tsne_image_visualization\backend\";

	public float displayimage_width = 1.00f;
	public float displayimage_height = 1.00f;

	public GameObject ImageDisplayPrefab;

	public GameObject ImageSpace;
	public GameObject room;

	private List<GameObject> objs;
	//display image lists
	//public List<GameObject>  displayimages  = new List<GameObject>();

	private float max_x = float.MinValue;
	private float min_x = float.MaxValue;

	private float max_y = float.MinValue;
	private float min_y = float.MaxValue;

	private float max_z = float.MinValue;
	private float min_z = float.MaxValue;

	void test ()
	{
		Renderer renderer = room.GetComponent<Renderer> ();
		Bounds combinedBounds = renderer.bounds;
		Component[] renderers = GetComponentsInChildren<Renderer> ();
		foreach (Renderer render in renderers) {
			if (render != renderer)
				combinedBounds.Encapsulate (render.bounds);
		}

		print (combinedBounds.ToString ());
	}
	// Use this for initialization
	void Start ()
	{
		//OVR
		OVRBoundary.BoundaryTestResult Testnode = new OVRBoundary.BoundaryTestResult ();
		objs = new List<GameObject> ();
		//OVRBoundary.
		//Bounds b = room.GetComponent<BoxCollider>().bounds;
		//print (room.GetComponent<Renderer> ().bounds.ToString ("F3"));
		//test ();
		//print (room.transform.localScale.ToString ("F3"));


		StartCoroutine (loadData (this.jsonFile));
	}
	
	// Update is called once per frame
	void Update ()
	{
		if (Input.GetKey (KeyCode.R)) {
			//StartCoroutine (ReloadAll ());
			StartCoroutine (rotateObjects ());
		}
	}


	private IEnumerator rotateObjects ()
	{
		if (this.busy) {
			yield break;
		}

		this.busy = true;
		print ("Starting to rotate");
		foreach (GameObject obj in objs) {
			obj.transform.Rotate (-GetNormalVector (obj.transform.GetComponent<SpriteRenderer> ().bounds) + obj.transform.position);
			yield return null;
		}
		this.busy = false;
	}


	public void OutputData ()
	{
		this.busy = true;
		for (int i = 0; i < this.transform.childCount; i++) {
			
		}
		this.busy = false;
	}

	public IEnumerator ReloadAll ()
	{
		if (this.busy) {
			yield break;
		}

		this.busy = true;

		for (int i = 0; i < this.transform.childCount; i++) {
			Destroy (this.transform.GetChild (0).gameObject);
			yield return null;
		}
		this.busy = false;
		Debug.Log ("Removed All images");

		StartCoroutine (loadData (this.jsonFile));
	}

	public Vector3 GetNormalVector (Bounds b)
	{
		float max_x = b.max.x;
		float max_y = b.max.y;

		float min_x = b.min.x;
		float min_y = b.min.y;

		float avg_z = b.max.z - ((b.max.z - b.min.z) / 2.0f);

		/*Vector3 max = new Vector3 (max_x, max_y, avg_z);
		Vector3 min = new Vector3 (min_x, min_y, avg_z);
		print ("max: " + max.ToString ("F3"));
		print ("min: " + min.ToString ("F3"));*/

		Vector3 vec1 = new Vector3 (max_x, max_y, avg_z);
		Vector3 vec2 = new Vector3 (min_x, max_y, avg_z);
		Vector3 vec3 = new Vector3 (max_x, min_y, avg_z);
		Vector3 vec4 = new Vector3 (min_x, min_y, avg_z);
		/*
		GameObject cube = GameObject.CreatePrimitive (PrimitiveType.Cube);
		cube.transform.position = vec1;
		cube.transform.localScale = new Vector3(0.25f,0.25f,0.25f);

		cube = GameObject.CreatePrimitive (PrimitiveType.Cube);
		cube.transform.position = vec2;
		cube.transform.localScale = new Vector3(0.25f,0.25f,0.25f);

		cube = GameObject.CreatePrimitive (PrimitiveType.Cube);
		cube.transform.position = vec3;
		cube.transform.localScale = new Vector3(0.25f,0.25f,0.25f);

		cube = GameObject.CreatePrimitive (PrimitiveType.Cube);
		cube.transform.position = vec4;
		cube.transform.localScale = new Vector3(0.25f,0.25f,0.25f);*/

		Vector3 norm = Vector3.Normalize (Vector3.Cross (vec1 - vec4, vec2 - vec4));
		//print ("Normal: " + norm.ToString ("F3"));
		//print ("Normal: " + norm.ToString ("F3"));
		return norm;
	}

	private void placeObject (Vector3 pos)
	{
		GameObject obj = GameObject.CreatePrimitive (PrimitiveType.Cube);
		obj.transform.position = pos;

	}

	private float translate (float min_val, float max_val, float new_min_val, float new_max_val, float val)
	{
		return ((new_max_val - new_min_val) * (val - min_val)) / (max_val - min_val) + new_min_val;
	}

	public void findMaxAndMin (string coordFile)
	{
		// load coordinates
		string dataAsJson = File.ReadAllText (coordFile);
		var N = JSON.Parse (dataAsJson);
		int j = 0;

		foreach (var key in N.Keys) {
			var coordinates = N [key] ["coordinates"];
			for (int i = 0; i < coordinates.Count; i++) {
				if (coordinates [i] ["x"] > max_x)
					max_x = coordinates [i] ["x"];
				if (coordinates [i] ["x"] < min_x)
					min_x = coordinates [i] ["x"];
				
				if (coordinates [i] ["y"] > max_y)
					max_y = coordinates [i] ["y"];
				if (coordinates [i] ["y"] < min_y)
					min_y = coordinates [i] ["y"];

				if (coordinates [i] ["z"] > max_z)
					max_z = coordinates [i] ["z"];
				if (coordinates [i] ["z"] < min_z)
					min_z = coordinates [i] ["z"];
			}
		}
		
//		placeObject (new Vector3(min_x, min_y, min_z));
//		placeObject (new Vector3(min_x, max_y, min_z));
//		placeObject (new Vector3(min_x, max_y, max_z));
//		placeObject (new Vector3(min_x, min_y, max_z));
//		placeObject (new Vector3(max_x, max_y, max_z));
//		placeObject (new Vector3(max_x, max_y, min_z));
//		placeObject (new Vector3(max_x, min_y, min_z));
//		placeObject (new Vector3(max_x, min_y, max_z));
//
//		float newMinX = translate (min_x, max_x, -1.5f, 1.5f, min_x);
//		float newMaxX = translate (min_x, max_x, -1.5f, 1.5f, max_x);
//
//		float newMinY = translate (min_y, max_y, 0.0f, 3.57f, min_y);
//		float newMaxY = translate (min_y, max_y, 0.0f, 3.57f, max_y);
//
//		float newMinZ = translate (min_z, max_z, 0.0f, 3.82f, min_z);
//		float newMaxZ = translate (min_z, max_z, 0.0f, 3.82f, max_z);
//
//		placeObject (new Vector3(newMinX, newMinY, newMinZ));
//		placeObject (new Vector3(newMinX, newMinY, newMaxZ));
//		placeObject (new Vector3(newMinX, newMaxY, newMinZ));
//		placeObject (new Vector3(newMinX, newMaxY, newMaxZ));
//		placeObject (new Vector3(newMaxX, newMinY, newMinZ));
//		placeObject (new Vector3(newMaxX, newMinY, newMaxZ));
//		placeObject (new Vector3(newMaxX, newMaxY, newMaxZ));
//		placeObject (new Vector3(newMaxX, newMaxY, newMinZ));

	}



	private Vector3 transformCoordinates (JSONNode ithNode)
	{
		float new_x = translate (min_x, max_x, -1.5f, 1.5f, ithNode ["x"]);
		float new_y = translate (min_y, max_y, 0.0f, 3.57f, ithNode ["y"]);
		float new_z = translate (min_z, max_z, 0.0f, 3.82f, ithNode ["z"]);
//		ithNode.Add()
		return new Vector3 (new_x, new_y, new_z);
	}

	public IEnumerator loadData (string coordFile)
	{
		if (this.busy) {
			yield break;
		}

		this.busy = true;

		findMaxAndMin (coordFile);
		// load coordinates
		string dataAsJson = File.ReadAllText (coordFile);

		var N = JSON.Parse (dataAsJson);
		int j = 0;
		foreach (var key in N.Keys) {
			var coordinates = N [key] ["coordinates"];
			//print ("key: " + key.ToString ());
//			for (int i = 0; i < coordinates.Count; i++) {
			for (int i = 0; i < 1 && coordinates.Count > 0; i++) {
				Vector3 pos = transformCoordinates (coordinates [i]);
				//Vector3 pos = new Vector3 (coordinates [i] ["x"], coordinates [i] ["y"], coordinates [i] ["z"]);
				pos.Scale (new Vector3 (this.scaleFactor, this.scaleFactor, this.scaleFactor));
				//set position
				//GameObject imageInstance = Instantiate (ImageDisplayPrefab, pos, Quaternion.identity);
				GameObject imageInstance = Instantiate (ImageDisplayPrefab);

				imageInstance.transform.SetParent (this.transform);
				imageInstance.transform.SetPositionAndRotation (pos, Quaternion.identity);

				ImageDisplayController controller = imageInstance.GetComponent<ImageDisplayController> ();

				string imagePath = this.imageFolder + key;

				int cropping_x = N [key] ["croppings"] [i] ["x"].AsInt;
				int cropping_y = N [key] ["croppings"] [i] ["y"].AsInt;
				int cropping_width = N [key] ["croppings"] [i] ["width"].AsInt;
				int cropping_height = N [key] ["croppings"] [i] ["height"].AsInt;

				controller.loadImage (imagePath, cropping_x, cropping_y, cropping_width, cropping_height);
				//controller.loadImage(imagePath);
				//scale the sprite Renderer so that all the sprint have same size 
				float sprite_x = imageInstance.GetComponent<SpriteRenderer> ().sprite.bounds.extents.x;  
				float sprite_y = imageInstance.GetComponent<SpriteRenderer> ().sprite.bounds.extents.y;



				Vector3 scale = new Vector3 (displayimage_width / sprite_x, displayimage_height / sprite_y, 1);

				imageInstance.transform.localScale = scale;
				//float diff = imageInstance.GetComponent<SpriteRenderer> ().bounds.max.x - imageInstance.GetComponent<SpriteRenderer> ().bounds.min.x;
				GetNormalVector (imageInstance.GetComponent<SpriteRenderer> ().bounds);
				objs.Add (imageInstance);

				//print ("bounds.min: " + imageInstance.GetComponent<SpriteRenderer> ().bounds.min.ToString ("F3"));
				//conlision
				//	Vector2 S = imageInstance.GetComponent<SpriteRenderer>().sprite.bounds.size;
				//	imageInstance.GetComponent<BoxCollider2D>().size = S;
				//imageInstance.GetComponent<BoxCollider2D>().offset = new Vector2 ((S.x / 2), 0);


				yield return null;
			}
			j++;
			if (j >= 100)
				break;
			yield return null;
		}

		this.busy = false;

	}
}

