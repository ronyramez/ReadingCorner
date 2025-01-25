import React from "react";
import { View, Image, StyleSheet } from "react-native";
import { StatusBar } from "expo-status-bar";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { CartProvider } from "../../context/CartContext";
import {
  DrawerContentScrollView,
  DrawerItemList,
  DrawerToggleButton,
} from "@react-navigation/drawer";
import { Drawer } from "expo-router/drawer";
import { SplashScreen, Link } from "expo-router";
import images from "@/constants/images";
import Toast from "react-native-toast-message";

SplashScreen.preventAutoHideAsync();

export default function Layout() {
  return (
    <>
      <CartProvider>
        <StatusBar style="light" backgroundColor="#6200ea" />
        <GestureHandlerRootView style={styles.gestureHandlerRootView}>
          <Drawer
            screenOptions={{
              drawerPosition: "right",
              drawerActiveTintColor: "#705C53",
              drawerInactiveTintColor: "#6F6F84",
              drawerActiveBackgroundColor: "#DBB5B5",
              headerStyle: styles.headerStyle,
              drawerStyle: { backgroundColor: "#F5F5F7" },
              headerTintColor: "#705C53",
              headerLeft: () => (
                <Link href={{ pathname: "./" }}>
                  <Image
                    source={images.logoSmall}
                    resizeMode="contain"
                    style={styles.logo}
                  />
                </Link>
              ),
              headerRight: () => (
                <View style={styles.drawerToggleButtonContainer}>
                  <DrawerToggleButton
                    tintColor="#705C53"
                    pressColor="#DBB5B5"
                  />
                </View>
              ),
            }}
          >
            <Drawer.Screen
              name="index"
              options={{
                drawerLabel: "Home",
                title: " ",
              }}
            />
            <Drawer.Screen
              name="explore"
              options={{
                drawerLabel: "Explore",
                title: " ",
              }}
            />
            <Drawer.Screen
              name="profile"
              options={{
                drawerLabel: "profile",
                title: " ",
              }}
            />
            <Drawer.Screen
              name="cart"
              options={{
                drawerLabel: "Cart",
                title: "Cart",
              }}
            />
            <Drawer.Screen
              name="order"
              options={{
                drawerLabel: "Order",
                title: " ",
              }}
            />
            <Drawer.Screen
              name="book"
              options={{
                drawerLabel: () => null,
                title: " ",
                drawerItemStyle: { height: 0 },
              }}
            />
          </Drawer>
        </GestureHandlerRootView>
      </CartProvider>
      <Toast />
    </>
  );
}

const styles = StyleSheet.create({
  gestureHandlerRootView: {
    flex: 1,
    backgroundColor: "#705C53",
  },
  headerStyle: {
    backgroundColor: "#F5F5F7",
    shadowColor: "transparent",
    height: 90,
  },
  logo: {
    width: 40,
    height: 35,
  },
  drawerToggleButtonContainer: {
    transform: [{ scaleX: -1 }],
    backgroundColor: "#F5F5F7",
  },
});
