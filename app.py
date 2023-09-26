from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from crop_test import find_crop

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/")
def get_crop_data():
    person1_collection = db.collection("person1")

    doc_ref = person1_collection.limit(1).get()
    data = {}
    for doc in doc_ref:
        data = doc.to_dict()

    n = data["N"]
    p = data["P"]
    k = data["K"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    ph = data["ph"]
    rainfall = data["rainfall"]

    crop = find_crop(n, p, k, temperature, humidity, ph, rainfall).capitalize()

    crop_data = {
        "crop": crop,
        "N": n,
        "P": p,
        "K": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }

    # Retrieve crop details and image from the database
    crop_details = get_crop_details(crop)
    crop_image_url = get_crop_image(crop)

    crop_data["details"] = crop_details
    crop_data["image_url"] = crop_image_url

    return jsonify(crop_data)


def get_crop_details(crop):
    crop_details = {
        "Rice": "Rice is a cereal grain that is grown in flooded fields. It is the staple food for most of the world's population, and is especially important in Asia and Africa. Rice is a good source of carbohydrates, and it also contains some protein and fiber.",
        "Maize": "Maize, also known as corn, is a cereal grain that is native to North America. It is a tall, grassy plant that produces ears of corn, which contain the kernels. Maize is a good source of carbohydrates, and it also contains some protein and fiber.",
        "Chickpea": "Chickpeas are a legume that is native to the Middle East. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Chickpeas can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Kidneybeans": "Kidney beans are a legume that is native to South America. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Kidney beans can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Pigeonpeas": "Pigeonpeas are a legume that is native to Africa. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Pigeonpeas can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Mothbeans": "Mothbeans are a legume that is native to India. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Mothbeans can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Mungbean": "Mungbeans are a legume that is native to Asia. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Mungbeans can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Blackgram": "Blackgram is a legume that is native to India. It is a good source of protein and fiber, and it is also a good source of vitamins and minerals. Blackgram can be eaten cooked or raw, and it is a versatile ingredient that can be used in many different dishes.",
        "Lentil": "Lentils are a legume that is native to the Middle East. They are a good source of protein and fiber, and they are also a good source of vitamins and minerals. Lentils can be eaten cooked or raw, and they are a versatile ingredient that can be used in many different dishes.",
        "Pomegranate": "Pomegranates are a fruit that is native to Iran. They are a good source of vitamins and minerals, and they also contain antioxidants. Pomegranates can be eaten fresh, or they can be used to make juice, jam, or jelly.",
        "Banana": "Bananas are a fruit that is native to Southeast Asia. They are a good source of carbohydrates, and they also contain some protein and fiber. Bananas can be eaten fresh, or they can be used to make banana bread, banana muffins, or banana ice cream.",
        "Mango": "Mangoes are a fruit that is native to India. They are a good source of vitamins and minerals, and they also contain antioxidants. Mangoes can be eaten fresh, or they can be used to make mango chutney, mango lassi, or mango ice cream.",
        "Grapes": "Grapes are a fruit that is native to Europe. They are a good source of carbohydrates, and they also contain some protein and fiber. Grapes can be eaten fresh, or they can be used to make wine, grape juice, or grape jelly.",
        "Watermelon": "Watermelon is a fruit that is native to Africa. It is a good source of water, and it also contains some vitamins and minerals. Watermelon can be eaten fresh, or it can be used to make watermelon juice or watermelon rind pickles.",
        "Muskmelon": "Muskmelon is a fruit that is native to India. It is a good source of vitamins and minerals, and it also contains antioxidants. Muskmelon can be eaten fresh, or it can be used to make muskmelon chutney or muskmelon ice cream.",
        "Apple": "Apples are a fruit that is native to Europe. They are a good source of vitamins and minerals, and they also contain antioxidants. Apples can be eaten fresh, or they can be used to make applesauce, apple pie, or apple cider.",
        "Orange": "Oranges are a fruit that is native to China. They are a good source of vitamins and minerals, and they also contain antioxidants. Oranges can be eaten fresh, or they can be used to make orange juice or orange marmalade.",
        "Papaya": "Papaya is a fruit that is native to Mexico. It is a good source of vitamins and minerals, and it also contains antioxidants. Papaya can be eaten fresh, or it can be used to make papaya chutney or papaya ice cream.",
        "Coconut": "Coconut is a fruit that is native to Southeast Asia. It is a good source of vitamins and minerals, and it also contains antioxidants. Coconut can be eaten fresh, or it can be used to make coconut milk or coconut oil.",
        "Cotton": "Cotton is a plant that is native to the Americas. It is a good source of fiber, and it also contains some protein. Cotton can be used to make clothing, bedding, or paper.",
        "Jute": "Jute is a plant that is native to India. It is a good source of fiber, and it also contains some protein. Jute can be used to make rope, twine, or burlap.",
        "Coffee": "Coffee is a plant that is native to Africa. It is a good source of caffeine, and it also contains some antioxidants. Coffee can be used to make coffee beans, coffee grounds, or coffee powder.",
    }
    print(crop)
    return crop_details.get(crop, "")


def get_crop_image(crop):
    crop_images = {
        "Rice": "https://images.unsplash.com/photo-1592997571659-0b21ff64313b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
        "Maize": "https://images.unsplash.com/photo-1604343574001-a9d95eb6384a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bWFpemV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
        "Chickpea": "https://plus.unsplash.com/premium_photo-1668420870598-e19f8d6d2019?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Y2hpY2twZWF8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
        "Kidney beans": "https://images.unsplash.com/photo-1513868853742-e7fb786265db?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8a2lkbmV5JTIwYmVhbnN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
        "Pigeonpeas": "https://specialtyproduce.com/sppics/11653.png",
        "Mothbeans": "https://media.istockphoto.com/id/1310610629/photo/full-frame-shot-of-turkish-gram-grains-forming-texture.jpg?s=612x612&w=0&k=20&c=bemtdsRUZQUZR97g1L4-cMBktDRnkNKZAWRwoRl8v1U=",
        "Mungbean": "https://cdn.britannica.com/12/158012-050-F79D3126/mung-beans-dishes-desserts-soups.jpg",
        "Blackgram": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Black_gram.jpg",
        "Lentil": "https://upload.wikimedia.org/wikipedia/commons/f/f5/3_types_of_lentil.png",
        "Pomegranate": "https://media.istockphoto.com/id/186548424/photo/pomegranate.jpg?s=612x612&w=0&k=20&c=IM6MPkr4hCp9jsaXMJ5cOsfeLfni31HV3cIqGLjroVQ=",
        "Banana": "https://images.everydayhealth.com/images/diet-nutrition/all-about-bananas-nutrition-facts-health-benefits-recipes-and-more-rm-722x406.jpg",
        "Mango": "https://cdn.britannica.com/05/75905-050-C7AE0733/Mangoes-tree.jpg",
        "Grapes": "https://images.pexels.com/photos/60021/grapes-wine-fruit-vines-60021.jpeg?cs=srgb&dl=pexels-pixabay-60021.jpg&fm=jpg",
        "Watermelon": "https://upload.wikimedia.org/wikipedia/commons/4/47/Taiwan_2009_Tainan_City_Organic_Farm_Watermelon_FRD_7962.jpg",
        "Muskmelon": "https://www.healthifyme.com/blog/wp-content/uploads/2020/04/Muskmelon-cover-1.jpg",
        "Apple": "https://cdn.britannica.com/22/187222-050-07B17FB6/apples-on-a-tree-branch.jpg",
        "Orange": "https://cdn.mos.cms.futurecdn.net/UaBq5LGpJQd3DDo6ve2dFW-1200-80.jpg",
        "Papaya": "https://cf.organicbazar.net/wp-content/uploads/2021/06/Untitled-design-2022-12-08T182126.753.jpg",
        "Coconut": "https://images.squarespace-cdn.com/content/v1/5c1074accc8fed6a4251da8f/1632825358284-7LGGMHZO98Q9L3FWUSKC/Coconut+Tree",
        "Cotton": "https://static.fibre2fashion.com/Newsresource/images/283/shutterstock-1823492183-1-_295312.jpg",
        "Jute": "https://media.istockphoto.com/id/1411013995/photo/green-jute-plantation-field-raw-jute-plant-texture-background.jpg?s=612x612&w=0&k=20&c=cqacEb83QgCc_CNw8VKEulIUgVl4dc9IDkjZR4JBEw0=",
        "Coffee": "https://images.pexels.com/photos/1695052/pexels-photo-1695052.jpeg?cs=srgb&dl=pexels-igor-haritanovich-1695052.jpg&fm=jpg",
    }

    return crop_images.get(crop, "")


if __name__ == "__main__":
    app.run(debug=True)
