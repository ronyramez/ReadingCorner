import React from "react";
import { Text, StyleSheet, ScrollView, Pressable, View } from "react-native";
import { RouteProp, useRoute } from "@react-navigation/native";
import { RootStackParamList } from "../../types";
import { useNavigation } from "@react-navigation/native";
import { LinearGradient } from "expo-linear-gradient";

type OrderScreenRouteProp = RouteProp<RootStackParamList, "order">;

const OrderScreen = () => {
  const route = useRoute<OrderScreenRouteProp>();
  const { totalPrice, books } = route.params;
  const navigation = useNavigation<any>();

  const handleBackToHome = () => {
    navigation.navigate("index");
  };

  return (
    <LinearGradient colors={["#705C53", "#5D4D46"]} style={styles.gradient}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.frame}>
          <View style={styles.card}>
            <Text style={styles.title}>Order Summary</Text>
            <View style={styles.totalContainer}>
              <Text style={styles.totalLabel}>Total Price</Text>
              <Text style={styles.totalPrice}>${totalPrice.toFixed(2)}</Text>
            </View>
            <View style={styles.booksContainer}>
              <View style={styles.booksHeader}>
                <Text style={styles.bookListTitle}>Books in your cart</Text>
                <View style={styles.bookCountBadge}>
                  <Text style={styles.bookCountText}>{books.length}</Text>
                </View>
              </View>
              {books.map((book, index) => (
                <View key={index} style={styles.bookItem}>
                  <View style={styles.bullet} />
                  <Text style={styles.bookName}>{book.title}</Text>
                </View>
              ))}
            </View>
            <Pressable
              style={({ pressed }) => [
                styles.backButton,
                pressed && styles.backButtonPressed,
              ]}
              onPress={handleBackToHome}
            >
              <Text style={styles.backButtonText}>Back to Home</Text>
            </Pressable>
          </View>
        </View>
      </ScrollView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  container: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
  },
  frame: {
    backgroundColor: "#705C53",
    borderRadius: 24,
    padding: 4,
    width: "100%",
    maxWidth: 408,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.2,
    shadowRadius: 5,
    elevation: 8,
  },
  card: {
    backgroundColor: "#EDDFE0",
    borderRadius: 20,
    padding: 24,
    width: "100%",
  },
  title: {
    fontSize: 28,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
    marginBottom: 24,
    textAlign: "center",
  },
  totalContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "baseline",
    marginBottom: 24,
  },
  totalLabel: {
    fontSize: 18,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
  },
  totalPrice: {
    fontSize: 24,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
  },
  booksContainer: {
    backgroundColor: "rgba(112, 92, 83, 0.1)",
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
  },
  booksHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  bookListTitle: {
    fontSize: 18,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
  },
  bookCountBadge: {
    backgroundColor: "#705C53",
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  bookCountText: {
    color: "#EDDFE0",
    fontSize: 14,
    fontFamily: "Poppins-SemiBold",
  },
  bookItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  bullet: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#705C53",
    marginRight: 8,
  },
  bookName: {
    fontSize: 16,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
  },
  backButton: {
    backgroundColor: "#705C53",
    padding: 16,
    borderRadius: 12,
    alignItems: "center",
  },
  backButtonPressed: {
    opacity: 0.9,
    transform: [{ scale: 0.98 }],
  },
  backButtonText: {
    color: "#EDDFE0",
    fontSize: 18,
    fontFamily: "Poppins-SemiBold",
  },
});

export default OrderScreen;
