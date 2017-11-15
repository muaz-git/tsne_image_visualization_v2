using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON;
using System.IO;

public class ImageManager : MonoBehaviour {

	public float scaleFactor = 0.2f;

	public bool busy = false;

	public string jsonFile = @"C:\Users\HP Sprout\Documents\Git Repositories\tsne_image_visualization\backend\data.json";
	public string imageFolder = @"C:\Users\HP Sprout\Documents\Git Repositories\tsne_image_visualization\backend\data\ImageNet";

	public GameObject ImageDisplayPrefab;

	public GameObject ImageSpace;

	// Use this for initialization
	void Start () {

		StartCoroutine(loadData(this.imageFolder, this.jsonFile));
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKey(KeyCode.R))
		{
			StartCoroutine(ReloadAll());
		}
	}

	public IEnumerator ReloadAll()
	{
		if (this.busy)
		{
			yield break;
		}

		this.busy = true;

		for (int i = 0; i < this.transform.childCount; i++)
		{
			Destroy(this.transform.GetChild(0).gameObject);
			yield return null;
		}
		this.busy = false;
		Debug.Log("Removed All images");

		StartCoroutine(loadData(this.imageFolder, this.jsonFile));
	}


	public IEnumerator loadData(string imageFolder, string coordFile)
	{
		if (this.busy)
		{
			yield break;
		}

		this.busy = true;

		// load coordinates
		string dataAsJson = File.ReadAllText(coordFile);

		var N = JSON.Parse(dataAsJson);

		foreach (var key in N.Keys)
		{
			var coordinates = N[key]["coordinates"];

			Vector3 pos = new Vector3(coordinates["x"], coordinates["y"], coordinates["z"]);
			pos.Scale(new Vector3(this.scaleFactor, this.scaleFactor, this.scaleFactor));

			//set position
			GameObject imageInstance = Instantiate(ImageDisplayPrefab, pos, Quaternion.identity);

			imageInstance.transform.SetParent(this.transform);
			imageInstance.transform.SetPositionAndRotation(pos, Quaternion.identity);

			ImageDisplayController controller = imageInstance.GetComponent<ImageDisplayController>();

			string imagePath = this.imageFolder + "\\" + key;
            controller.loadImage(imagePath);

			yield return null;
		}

		this.busy = false;

	}
}
