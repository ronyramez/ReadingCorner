import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  Pressable,
} from "react-native";
import { useCart } from "../../context/CartContext";
import { useNavigation, NavigationProp } from "@react-navigation/native";
import { RootStackParamList } from "../../types";

const CartScreen = () => {
  const { cart, removeFromCart } = useCart();
  const navigation = useNavigation<NavigationProp<RootStackParamList>>();

  const handleRemove = (bookId: number) => {
    removeFromCart(bookId);
  };

  const handleCheckout = () => {
    const totalPrice = cart.reduce((sum, book) => sum + book.price, 0);
    navigation.navigate("order", { totalPrice, books: cart });
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {cart.length > 0 ? (
        <>
          {cart.map((book, index) => (
            <View key={index} style={styles.bookItem}>
              <Image source={book.image} style={styles.bookImage} />
              <View style={styles.bookDetails}>
                <Text style={styles.bookTitle}>{book.title}</Text>
                <Text style={styles.bookAuthor}>{book.author}</Text>
                <Text style={styles.bookPrice}>${book.price}</Text>
                <Pressable
                  onPress={() => handleRemove(Number(book.id))}
                  style={styles.Button}
                >
                  <Image
                    source={require("@/assets/icons/trash.png")}
                    style={styles.buttonIcon}
                  />
                </Pressable>
              </View>
            </View>
          ))}
          <Pressable style={styles.checkoutButton} onPress={handleCheckout}>
            <Text style={styles.checkoutButtonText}>Checkout</Text>
          </Pressable>
        </>
      ) : (
        <Text style={styles.emptyCartText}>Your cart is empty</Text>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 16,
    backgroundColor: "#F5F5F7",
  },
  sectionTitle: {
    fontSize: 24,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
    marginBottom: 20,
    textAlign: "center",
  },
  bookItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 20,
    backgroundColor: "#FFF",
    padding: 10,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  bookImage: {
    width: 60,
    height: 90,
    borderRadius: 4,
    marginRight: 10,
  },
  bookDetails: {
    flex: 1,
  },
  bookTitle: {
    fontSize: 18,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
  },
  bookAuthor: {
    fontSize: 14,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
    marginBottom: 5,
  },
  bookPrice: {
    fontSize: 16,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
  },
  emptyCartText: {
    fontSize: 16,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
    textAlign: "center",
    marginTop: 16,
  },
  Button: {
    backgroundColor: "#E7CACC",
    color: "#705C53",
    padding: 10,
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    width: 30,
    left: 220,
    height: 30,
  },
  buttonIcon: {
    width: 20,
    height: 20,
    right: 5,
    top: -5,
    tintColor: "#705C53",
  },
  checkoutButton: {
    backgroundColor: "#E7CACC",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
    marginTop: 20,
  },
  checkoutButtonText: {
    color: "#705C53",
    fontSize: 16,
  },
});

export default CartScreen;
