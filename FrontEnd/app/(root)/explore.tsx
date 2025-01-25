import React, { useState } from "react";
import {
  ScrollView,
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  TextInput,
} from "react-native";
import { useRouter } from "expo-router";
import { books } from "@/constants/mockdata";
import ExploreBooks from "@/components/home/exploreBooks";

const Categories = () => {
  const router = useRouter();
  const [searchMode, setSearchMode] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const handelSearch = (query: string) => {
    setSearchQuery(query);
    query.length > 0 ? setSearchMode(true) : setSearchMode(false);
  };
  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const groupedBooks = books.reduce(
    (acc: { [key: string]: any[] }, book: any) => {
      if (!acc[book.category]) {
        acc[book.category] = [];
      }

      acc[book.category].push(book);

      return acc;
    },
    {}
  );

  return (
    <ScrollView style={styles.container}>
      <TextInput
        style={styles.searchInput}
        placeholderTextColor={"#705C53"}
        placeholder="👀 Look for books, authors...."
        value={searchQuery}
        onChangeText={(text) => {
          handelSearch(text);
        }}
      />
      {!searchMode &&
        Object.keys(groupedBooks).map((category) => (
          <View key={category} style={styles.categoryContainer}>
            <Text style={styles.categoryTitle}>{category}</Text>
            <View style={{ paddingLeft: 16 }}>
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                {groupedBooks[category].map((book) => (
                  <TouchableOpacity
                    key={book.id}
                    style={styles.bookItem}
                    onPress={() =>
                      router.push({
                        pathname: "./book",
                        params: { book: JSON.stringify(book) },
                      })
                    }
                  >
                    <Image
                      source={book.image}
                      style={styles.bookImage}
                      resizeMode="cover"
                    />
                    <Text style={styles.bookTitle}>{book.title}</Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>
            </View>
          </View>
        ))}
      {searchMode &&
        (filteredBooks.length > 0 ? (
          <ExploreBooks books={filteredBooks} />
        ) : (
          <Text style={styles.notFoundText}>No books are found</Text>
        ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F5F7",
  },
  searchInput: {
    color: "#705C53",
    backgroundColor: "#B7B7B7",
    borderColor: "#705C53",
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
    margin: 16,
    fontSize: 16,
  },
  categoryContainer: {
    marginBottom: 20,
  },
  categoryTitle: {
    fontSize: 20,
    fontFamily: "Poppins-SemiBold",
    color: "#705C53",
    marginLeft: 16,
    marginBottom: 10,
  },
  bookItem: {
    marginRight: 16,
    alignItems: "center",
  },
  bookImage: {
    width: 100,
    height: 150,
    borderRadius: 8,
  },
  bookTitle: {
    marginTop: 8,
    fontSize: 14,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
    textAlign: "center",
  },
  notFoundText: {
    fontSize: 16,
    fontFamily: "Poppins-Regular",
    color: "#705C53",
    textAlign: "center",
    marginTop: 16,
  },
});

export default Categories;
