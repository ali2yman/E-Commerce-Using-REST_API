from rest_framework import serializers
from .models import Product,Review



# the ProductSerializer includes a custom field reviews that dynamically retrieves and serializes reviews associated with each product 
# using the ReviewSerializer. This allows the product API endpoint to provide information about associated reviews along with product details.


class ProductSerializer(serializers.ModelSerializer):
    
    reviews = serializers.SerializerMethodField(method_name='get_reviews',read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
      #  fields = ('name', 'price','brand')

# method is defined to retrieve all reviews associated with a product and serialize them using the ReviewSerializer
    def get_reviews(self,obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
     