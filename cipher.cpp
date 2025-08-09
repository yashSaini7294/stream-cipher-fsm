#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <random>
#include <string>

// ------------------------
// PRNG: Linear Feedback Shift Register (8-bit)
// ------------------------
class PRNG {
private:
    uint8_t state;

public:
    PRNG(uint8_t seed) : state(seed) {}

    uint8_t next() {
    // Convert state to bit array
    bool bits[8];
    for (int i = 0; i < 8; ++i)
        bits[i] = (state >> (7 - i)) & 1;

    // XOR the selected taps: 7, 5, 4, 3
    bool feedback = bits[0] ^ bits[2] ^ bits[3] ^ bits[4];

    // Shift left and add feedback
    state = (state << 1) | feedback;
    return state;
	}

};

// ------------------------
// Stream Cipher FSM
// ------------------------
class StreamCipher {
private:
    PRNG prng;

public:
    StreamCipher(uint8_t seed) : prng(seed) {}

    std::vector<uint8_t> process(const std::vector<uint8_t>& input) {
        std::vector<uint8_t> output;
        for (uint8_t byte : input) {
            uint8_t keystream = prng.next();
            output.push_back(byte ^ keystream);  // XOR with keystream
        }
        return output;
    }
};

// ------------------------
// File Read/Write Helpers
// ------------------------
std::vector<uint8_t> read_file(const std::string& filename) {
    std::vector<uint8_t> data;
    std::ifstream file(filename, std::ios::binary);
    uint8_t byte;
    while (file.read(reinterpret_cast<char*>(&byte), 1)) {
        data.push_back(byte);
    }
    return data;
}

void write_file(const std::string& filename, const std::vector<uint8_t>& data) {
    std::ofstream file(filename, std::ios::binary);
    for (uint8_t byte : data) {
        file.write(reinterpret_cast<const char*>(&byte), 1);
    }
}

// ------------------------
// Entry Point
// ------------------------
// Usage:
// ./cipher input.txt output.txt 123
int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: ./cipher <input_file> <output_file> <seed>\n";
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];
    int seed = std::stoi(argv[3]);

    // Read input
    std::vector<uint8_t> input_data = read_file(input_file);

    // Encrypt/Decrypt using FSM stream cipher
    StreamCipher cipher(seed);
    std::vector<uint8_t> output_data = cipher.process(input_data);

    // Write output
    write_file(output_file, output_data);

    return 0;
}