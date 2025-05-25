def lambda_handler(event, context):
    try:
        from PIL import Image
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}
