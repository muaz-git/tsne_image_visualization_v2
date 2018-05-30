using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON;
using System.IO;

public class InputManager2 : MonoBehaviour
{
	public class MyObject
	{
		public JSONNode myNode;
		public GameObject gObj;
		public string key;

		public MyObject (JSONNode content, GameObject myobj, string k)
		{
			this.gObj = myobj;
			this.key = k;
			this.myNode = content;
		}


	}

	public GameObject ImageDisplayPrefab;
	public float scaleFactor = 0.2f;

	private List<MyObject> objs;
	private string jsonFile = @"C:\Workspaces\Muaz\tsne_image_visualization_v2\backend\temp.json";
	private string updatedJsonFile = @"C:\Workspaces\Muaz\tsne_image_visualization_v2\backend\temp_updated.json";
	private string imageFolder = @"C:\Users\IML\tsne_image_visualization\backend\";
	private bool busy = false;
	private float displayimage_width = 0.05f;
	private float displayimage_height = 0.05f;

	private float max_x = float.MinValue;
	private float min_x = float.MaxValue;
	private float max_y = float.MinValue;
	private float min_y = float.MaxValue;
	private float max_z = float.MinValue;
	private float min_z = float.MaxValue;

	private float newMin_x;
	private float newMax_x;
	private float newMin_y;
	private float newMax_y;
	private float newMin_z;
	private float newMax_z;

	private void init ()
	{
		objs = new List<MyObject> ();
		newMin_x = -1.5f;
		newMax_x = 1.5f;
		newMin_y = 0.0f;
		newMax_y = 3.57f;
		newMin_z = 0.0f;
		newMax_z = 3.82f;
	}

	void Start ()
	{
//		print ("Application.dataPath: "+Application.);
//		if (File.Exists (this.updatedJsonFile))
//			File.Delete (this.updatedJsonFile);
		init ();
		this.loadFile ();

	}

	public void loadFile ()
	{
		if (File.Exists (this.updatedJsonFile))
			StartCoroutine (loadFromUpdated (this.updatedJsonFile));
		else
			StartCoroutine (loadFromOriginal (this.jsonFile));
	}

	// transform position vector,
	// scale position vector,
	// create image object at position vector,
	// scale image object
	// add new position to nthNode of JSON.
	private GameObject createGameObject (JSONNode nthNode, string key, int i)
	{
		Vector3 pos;
		Quaternion quat;
		if (nthNode ["new_position"] != null) { // if node is updated
			pos = JSONNodeToVector3 (nthNode ["new_position"] [0]); // because "new_position is JSONArray"
			quat = JSONNodeToQuaternion (nthNode ["new_rotation"] [0]); // because "new_rotation is JSONArray"
			print(quat.ToString());

		} else {
			pos = transformCoordinates (nthNode ["coordinates"] [i]);
			pos.Scale (new Vector3 (this.scaleFactor, this.scaleFactor, this.scaleFactor));
			quat = Quaternion.identity;
		}
		GameObject imageInstance = Instantiate (ImageDisplayPrefab);
		imageInstance.transform.SetParent (this.transform);
		imageInstance.transform.SetPositionAndRotation (pos, quat);
		ImageDisplayController controller = imageInstance.GetComponent<ImageDisplayController> ();

		string imagePath = this.imageFolder + key;

		int cropping_x = nthNode ["croppings"] [i] ["x"].AsInt;
		int cropping_y = nthNode ["croppings"] [i] ["y"].AsInt;
		int cropping_width = nthNode ["croppings"] [i] ["width"].AsInt;
		int cropping_height = nthNode ["croppings"] [i] ["height"].AsInt;

		controller.loadImage (imagePath, cropping_x, cropping_y, cropping_width, cropping_height);

		//scale the sprite Renderer so that all the sprint have same size 
		float sprite_x = imageInstance.GetComponent<SpriteRenderer> ().sprite.bounds.extents.x;  
		float sprite_y = imageInstance.GetComponent<SpriteRenderer> ().sprite.bounds.extents.y;



		Vector3 scale = new Vector3 (displayimage_width / sprite_x, displayimage_height / sprite_y, 1);

		imageInstance.transform.localScale = scale;

		return imageInstance;
	}

	private IEnumerator loadFromOriginal (string filename)
	{
		if (this.busy) {
			yield break;
		}

		this.busy = true;

		findMaxAndMin (filename);

		string dataAsJson = File.ReadAllText (filename);
		var N = JSON.Parse (dataAsJson);
		int j = 0;
		foreach (var key in N.Keys) {
			JSONNode nthNode = N [key];
			//var coordinates = N [key] ["coordinates"];
			if (nthNode ["coordinates"].Count > 0) { // iterating over only one coordinate
				//			for (int i = 0; i < nthNode ["coordinates"].Count; i++) {
				// transform coordinate
				// add transform coordinate to ith JSON object



				// create Game object from prefab
				GameObject gameObjRef = createGameObject (nthNode, key, 0);

				// Create object of MyObject and add ith JSON object and Game object to MyObject
				MyObject obj = new MyObject (nthNode, gameObjRef, key);
				// add MyObject to obj list
				objs.Add (obj);

			}
			j++;
			if (j > 2)
				break;
			yield return null;
		}
		this.busy = false;
	}

	public IEnumerator loadFromUpdated (string filename)
	{
		if (this.busy) {
			yield break;
		}

		this.busy = true;
		string dataAsJson = File.ReadAllText (filename);
		var N = JSON.Parse (dataAsJson);


		for (int i = 0; i < N.Count; i++) { // N is JSONArray
			foreach (var key in N[i].Keys) { 
				
				JSONNode nthNode = N [i] [key];


				GameObject gameObjRef = createGameObject (nthNode, key, 0);
				MyObject obj = new MyObject (nthNode, gameObjRef, key);
				// add MyObject to obj list
				objs.Add (obj);

			}
			yield return null;	
		}
		this.busy = false;
	}

	private Vector3 transformCoordinates (JSONNode ithNode)
	{
		float new_x = translate (min_x, max_x, newMin_x, newMax_x, ithNode ["x"]);
		float new_y = translate (min_y, max_y, newMin_y, newMax_y, ithNode ["y"]);
		float new_z = translate (min_z, max_z, newMin_z, newMax_z, ithNode ["z"]);

		return new Vector3 (new_x, new_y, new_z);
	}

	private float translate (float min_val, float max_val, float new_min_val, float new_max_val, float val)
	{
		return ((new_max_val - new_min_val) * (val - min_val)) / (max_val - min_val) + new_min_val;
	}

	private void findMaxAndMin (string coordFile)
	{
		// load coordinates
		string dataAsJson = File.ReadAllText (coordFile);
		var N = JSON.Parse (dataAsJson);
		int j = 0;

		foreach (var key in N.Keys) {
			var coordinates = N [key] ["coordinates"];
			if (N [key] ["coordinates"].Count > 0) {
				int i = 0;
//			for (int i = 0; i < coordinates.Count; i++) {
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
				j++;
			}

		}
	}

	private void placeObject (Vector3 pos)
	{
		GameObject obj = GameObject.CreatePrimitive (PrimitiveType.Cube);
		obj.transform.position = pos;
	}

	private JSONNode Vector3ToJSONNode (Vector3 v)
	{
		JSONNode objData = new JSONObject ();
		objData ["x"] = v.x;
		objData ["y"] = v.y;
		objData ["z"] = v.z;

		return objData;
	}

	private JSONNode QuaternionToJSONNode (Quaternion q)
	{
		JSONNode objData = new JSONObject ();
		objData ["w"] = q.w;
		objData ["x"] = q.x;
		objData ["y"] = q.y;
		objData ["z"] = q.z;

		return objData;
	}

	private Quaternion JSONNodeToQuaternion (JSONNode nd)
	{
		return new Quaternion (nd ["x"], nd ["y"], nd ["z"], nd ["w"]);
	}

	private Vector3 JSONNodeToVector3 (JSONNode nd)
	{
		return new Vector3 (nd ["x"], nd ["y"], nd ["z"]); // because "new_position is JSONArray"
	}

	private void writeJSONToFile (JSONNode obj)
	{
		File.WriteAllText (this.updatedJsonFile, obj.ToString ());
	}

	void OnApplicationQuit ()
	{
		JSONNode objData = new JSONArray ();

		foreach (MyObject obj in objs) {
			// adding scaled position to nthNode
			obj.myNode ["new_position"] = new JSONArray ();
			obj.myNode ["new_position"].Add (Vector3ToJSONNode (FixPositionVector (obj.gObj.transform.position)));

			obj.myNode ["new_rotation"] = new JSONArray ();
			obj.myNode ["new_rotation"].Add (QuaternionToJSONNode(obj.gObj.transform.localRotation));

			JSONNode tmpObj = new JSONObject ();
			tmpObj [obj.key] = obj.myNode;
			objData.Add (tmpObj);


		}
		writeJSONToFile (objData);
	}

	private Vector3 FixPositionVector (Vector3 v)
	{
		return v;
	}
}
