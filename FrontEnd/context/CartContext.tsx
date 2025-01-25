import React, { createContext, useState, useContext, ReactNode } from "react";
import { ImageSourcePropType } from "react-native";

type Book = {
  id: number;
  title: string;
  author: string;
  price: number;
  image: ImageSourcePropType;
};
type CartContextType = {
  cart: Book[];
  addToCart: (book: Book) => void;
  removeFromCart: (bookId: number) => void;
};

const CartContext = createContext<CartContextType>({
  cart: [],
  addToCart: () => {},
  removeFromCart: () => {},
});

export const CartProvider = ({ children }: { children: ReactNode }) => {
  const [cart, setCart] = useState<Book[]>([]);

  const addToCart = (book: Book) => {
    setCart((prevCart) => [...prevCart, book]);
  };
  const removeFromCart = (bookId: number) => {
    setCart((prevCart) => prevCart.filter((book) => book.id !== bookId));
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
