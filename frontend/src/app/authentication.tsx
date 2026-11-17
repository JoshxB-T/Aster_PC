import React, { useState } from "react";

import {
    ActivityIndicator,
    KeyboardAvoidingView,
    Platform,
    Pressable,
    ScrollView,
    StyleSheet,
    Text,
    TextInput,
    View,
} from "react-native";

import { postSignup } from "../../api/signupService";
import { router } from "expo-router";
import { useAuth } from '../contexts/AuthContext';

type AuthMode = "login" | "signup";

export default function AuthenticationScreen() {
    const [mode, setMode] = useState<AuthMode>("login");

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const { signIn } = useAuth();

    const resetMessages = () => {
        setError("");
        setSuccess("");
    };

    const switchMode = (newMode: AuthMode) => {
        setMode(newMode);
        resetMessages();
        setPassword("");
        setConfirmPassword("");
    };

    const validateForm = (): boolean => {
        if (mode === "signup" && !username.trim()) {
            setError("Please enter your username.");
            return false;
        }

        if (!email.trim()) {
            setError("Please enter your email.");
            return false;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
            setError("Please enter a valid email address.");
            return false;
        }

        if (!password) {
            setError("Please enter your password.");
            return false;
        }

        if (password.length < 8) {
            setError("Password must contain at least 8 characters.");
            return false;
        }

        if (mode === "signup" && password !== confirmPassword) {
            setError("Passwords do not match.");
            return false;
        }

        return true;
    };


    const handleSubmit = async () => {
        resetMessages();

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        try {
            if (mode === "login") {
                await signIn({
                    email: email.trim(),
                    password: password
                });

                router.replace("/(tabs)");
            } else {
                const response = await postSignup({
                    username: username.trim(),
                    email: email.trim(),
                    password: password
                });

                console.log("Signup success: ", response);

                setMode("login");
            }
        } catch (err) {
            setError("Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    };


    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === "ios" ? "padding" : undefined}
        >
            <ScrollView
                contentContainerStyle={styles.scrollContent}
                keyboardShouldPersistTaps="handled"
            >
                <View style={styles.formContainer}>

                    {/* Application branding */}
                    <View style={styles.header}>
                        <Text style={styles.title}>
                            {mode === "login"
                                ? "Welcome back"
                                : "Create an account"}
                        </Text>

                        <Text style={styles.subtitle}>
                            {mode === "login"
                                ? "Sign in to continue to your account."
                                : "Enter your details to get started."}
                        </Text>
                    </View>


                    {/* Authentication mode selector */}
                    <View style={styles.modeSelector}>
                        <Pressable
                            style={[
                                styles.modeButton,
                                mode === "login" && styles.activeMode,
                            ]}
                            onPress={() => switchMode("login")}
                        >
                            <Text
                                style={[
                                    styles.modeText,
                                    mode === "login" && styles.activeModeText,
                                ]}
                            >
                                Login
                            </Text>
                        </Pressable>

                        <Pressable
                            style={[
                                styles.modeButton,
                                mode === "signup" && styles.activeMode,
                            ]}
                            onPress={() => switchMode("signup")}
                        >
                            <Text
                                style={[
                                    styles.modeText,
                                    mode === "signup" && styles.activeModeText,
                                ]}
                            >
                                Sign Up
                            </Text>
                        </Pressable>
                    </View>


                    {/* Form fields */}
                    <View style={styles.form}>

                        {mode === "signup" && (
                            <View style={styles.inputGroup}>
                                <Text style={styles.label}>Username</Text>

                                <TextInput
                                    style={styles.input}
                                    placeholder="Enter your username"
                                    placeholderTextColor="#888"
                                    value={username}
                                    onChangeText={setUsername}
                                    autoCapitalize="words"
                                    editable={!loading}
                                />
                            </View>
                        )}


                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Email Address</Text>

                            <TextInput
                                style={styles.input}
                                placeholder="user@example.com"
                                placeholderTextColor="#888"
                                value={email}
                                onChangeText={setEmail}
                                keyboardType="email-address"
                                autoCapitalize="none"
                                autoCorrect={false}
                                editable={!loading}
                            />
                        </View>


                        <View style={styles.inputGroup}>
                            <Text style={styles.label}>Password</Text>

                            <View style={styles.passwordContainer}>
                                <TextInput
                                    style={styles.passwordInput}
                                    placeholder="Enter your password"
                                    placeholderTextColor="#888"
                                    value={password}
                                    onChangeText={setPassword}
                                    secureTextEntry={!showPassword}
                                    autoCapitalize="none"
                                    editable={!loading}
                                />

                                <Pressable
                                    onPress={() => setShowPassword(!showPassword)}
                                >
                                    <Text style={styles.togglePassword}>
                                        {showPassword ? "Hide" : "Show"}
                                    </Text>
                                </Pressable>
                            </View>
                        </View>


                        {mode === "signup" && (
                            <View style={styles.inputGroup}>
                                <Text style={styles.label}>
                                    Confirm Password
                                </Text>

                                <TextInput
                                    style={styles.input}
                                    placeholder="Confirm your password"
                                    placeholderTextColor="#888"
                                    value={confirmPassword}
                                    onChangeText={setConfirmPassword}
                                    secureTextEntry={!showPassword}
                                    autoCapitalize="none"
                                    editable={!loading}
                                />
                            </View>
                        )}


                        {/* Feedback messages */}
                        {!!error && (
                            <Text style={styles.errorMessage}>
                                {error}
                            </Text>
                        )}

                        {!!success && (
                            <Text style={styles.successMessage}>
                                {success}
                            </Text>
                        )}


                        {/* Submit button */}
                        <Pressable
                            style={[
                                styles.submitButton,
                                loading && styles.disabledButton,
                            ]}
                            onPress={handleSubmit}
                            disabled={loading}
                        >
                            {loading ? (
                                <ActivityIndicator color="#FFFFFF" />
                            ) : (
                                <Text style={styles.submitButtonText}>
                                    {mode === "login"
                                        ? "Sign In"
                                        : "Create Account"}
                                </Text>
                            )}
                        </Pressable>


                        {/* Mode switching */}
                        <View style={styles.footer}>
                            <Text style={styles.footerText}>
                                {mode === "login"
                                    ? "Don't have an account? "
                                    : "Already have an account? "}
                            </Text>

                            <Pressable
                                onPress={() =>
                                    switchMode(
                                        mode === "login" ? "signup" : "login"
                                    )
                                }
                            >
                                <Text style={styles.footerLink}>
                                    {mode === "login" ? "Sign Up" : "Login"}
                                </Text>
                            </Pressable>
                        </View>

                    </View>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#F4F6FA",
    },

    scrollContent: {
        flexGrow: 1,
        justifyContent: "center",
        padding: 24,
    },

    formContainer: {
        width: "100%",
        maxWidth: 450,
        alignSelf: "center",
        backgroundColor: "#FFFFFF",
        borderRadius: 16,
        padding: 28,
        elevation: 3,
        shadowColor: "#000",
        shadowOpacity: 0.08,
        shadowRadius: 12,
        shadowOffset: { width: 0, height: 4 },
    },

    header: {
        alignItems: "center",
        marginBottom: 28,
    },

    logo: {
        fontSize: 14,
        fontWeight: "800",
        letterSpacing: 2,
        color: "#3157A4",
        marginBottom: 18,
    },

    title: {
        fontSize: 26,
        fontWeight: "700",
        color: "#1C2434",
        marginBottom: 8,
    },

    subtitle: {
        fontSize: 14,
        color: "#747D8C",
        textAlign: "center",
    },

    modeSelector: {
        flexDirection: "row",
        backgroundColor: "#F0F2F6",
        borderRadius: 10,
        padding: 4,
        marginBottom: 26,
    },

    modeButton: {
        flex: 1,
        alignItems: "center",
        paddingVertical: 12,
        borderRadius: 8,
    },

    activeMode: {
        backgroundColor: "#3157A4",
    },

    modeText: {
        fontSize: 14,
        fontWeight: "600",
        color: "#687386",
    },

    activeModeText: {
        color: "#FFFFFF",
    },

    form: {
        gap: 18,
    },

    inputGroup: {
        gap: 8,
    },

    label: {
        fontSize: 14,
        fontWeight: "600",
        color: "#344054",
    },

    input: {
        height: 50,
        borderWidth: 1,
        borderColor: "#D9DEE8",
        borderRadius: 9,
        paddingHorizontal: 14,
        fontSize: 15,
        color: "#1C2434",
        backgroundColor: "#FFFFFF",
    },

    passwordContainer: {
        height: 50,
        flexDirection: "row",
        alignItems: "center",
        borderWidth: 1,
        borderColor: "#D9DEE8",
        borderRadius: 9,
        paddingHorizontal: 14,
    },

    passwordInput: {
        flex: 1,
        fontSize: 15,
        color: "#1C2434",
    },

    togglePassword: {
        color: "#3157A4",
        fontSize: 13,
        fontWeight: "600",
        paddingLeft: 10,
    },

    errorMessage: {
        color: "#D92D20",
        fontSize: 13,
    },

    successMessage: {
        color: "#16803C",
        fontSize: 13,
    },

    submitButton: {
        height: 52,
        backgroundColor: "#3157A4",
        borderRadius: 9,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 6,
    },

    disabledButton: {
        opacity: 0.6,
    },

    submitButtonText: {
        color: "#FFFFFF",
        fontSize: 15,
        fontWeight: "700",
    },

    footer: {
        flexDirection: "row",
        justifyContent: "center",
        marginTop: 8,
    },

    footerText: {
        color: "#747D8C",
        fontSize: 13,
    },

    footerLink: {
        color: "#FF0000",
        fontSize: 13,
        fontWeight: "700",
    },
});
