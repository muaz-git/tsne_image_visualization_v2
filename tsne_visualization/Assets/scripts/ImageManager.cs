using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON;
using System.IO;

public class ImageManager : MonoBehaviour {

	public float scaleFactor = 0.2f;

	public string jsonFile = @"C:\Users\HP Sprout\Documents\Git Repositories\tsne_image_visualization\backend\data.json";
	public string imageFolder = @"C:\Users\HP Sprout\Documents\Git Repositories\tsne_image_visualization\backend\data\ImageNet";

	public GameObject ImageDisplayPrefab;

	public GameObject ImageSpace;

	// Use this for initialization
	void Start () {

		loadData(this.imageFolder, this.jsonFile);
	}
	
	// Update is called once per frame
	void Update () {
		
	}


	public void loadData(string imageFolder, string coordFile)
	{
		// load coordinates
		string dataAsJson = File.ReadAllText(coordFile);

		var N = JSON.Parse(dataAsJson);

		foreach (var key in N.Keys)
		{
			var coordinates = N[key];

			Debug.Log(key + " - x:" + coordinates[0] + " y:" + coordinates[1] + " z:" + coordinates[2]);

			Vector3 pos = new Vector3(coordinates[0], coordinates[1], coordinates[2]);
			pos.Scale(new Vector3(this.scaleFactor, this.scaleFactor, this.scaleFactor));

			//set position
			GameObject imageInstance = Instantiate(ImageDisplayPrefab, pos, Quaternion.identity);

			imageInstance.transform.SetParent(this.transform);
			imageInstance.transform.SetPositionAndRotation(pos, Quaternion.identity);

			ImageDisplayController controller = imageInstance.GetComponent<ImageDisplayController>();

			string imagePath = this.imageFolder + "\\" + key;
            controller.loadImage(imagePath);

        }

	}
}
