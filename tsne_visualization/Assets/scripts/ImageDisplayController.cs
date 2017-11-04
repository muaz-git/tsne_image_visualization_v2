using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ImageDisplayController : MonoBehaviour {

	SpriteRenderer imageSprite;

	public void loadImage(string FilePath, float PixelsPerUnit=100.0f)
	{
		// Load a PNG or JPG image from disk to a Texture2D, assign this texture to a new sprite and return its reference

		Sprite NewSprite = new Sprite();
		Texture2D SpriteTexture = LoadTexture(FilePath);
		NewSprite = Sprite.Create(SpriteTexture, new Rect(0, 0, SpriteTexture.width, SpriteTexture.height), new Vector2(0, 0), PixelsPerUnit);

		this.imageSprite = this.gameObject.GetComponent<SpriteRenderer>();
		this.imageSprite.sprite = NewSprite;
	}

	public Texture2D LoadTexture(string FilePath)
	{

		// Load a PNG or JPG file from disk to a Texture2D
		// Returns null if load fails

		Texture2D Tex2D;
		byte[] FileData;

		if (File.Exists(FilePath))
		{
			FileData = File.ReadAllBytes(FilePath);
			Tex2D = new Texture2D(2, 2);           // Create new "empty" texture
			if (Tex2D.LoadImage(FileData))           // Load the imagedata into the texture (size is set automatically)
				return Tex2D;                 // If data = readable -> return texture
		}
		return null;                     // Return null if load failed
	}

	public void setPosition(float x, float y, float z)
	{
		transform.position = new Vector3(x, y, z);
	}

	// Use this for initialization
	void Start () {
		this.imageSprite = this.gameObject.GetComponent<SpriteRenderer>();
    }
	
	// Update is called once per frame
	void Update () {
		
	}
}
