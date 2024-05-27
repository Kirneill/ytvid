#include <iostream>
#include <fstream>
#include <cstdlib>
#include <filesystem>
#include <array>
#include <memory>

namespace fs = std::filesystem;

// Utilizing system commands for ffmpeg and whisper.cpp operations
std::string run_command(const std::string& cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(cmd.c_str(), "r"), _pclose);
    if (!pipe) {
        std::cerr << "Failed to run command: " << cmd << std::endl;
        return "";
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    if (result.empty()) {
        std::cerr << "No output from command: " << cmd << std::endl;
    }
    return result;
}

// Convert video to wav using ffmpeg
std::string convert_video_to_wav(const std::string& video_path, const std::string& ffmpeg_path) {
    std::string wav_path = video_path.substr(0, video_path.size() - 4) + ".wav";
    std::string command = ffmpeg_path + " -i " + video_path + " " + wav_path;
    std::string result = run_command(command);
    if (result.empty()) {
        std::cerr << "Failed to convert video to WAV: " << video_path << std::endl;
    }
    return wav_path;
}

// Transcribe video using whisper.cpp
std::string transcribe_video(const std::string& wav_path, const std::string& model_path, const std::string& whisper_cpp_path) {
    std::string whisper_executable = whisper_cpp_path + "/main";
    std::string command = whisper_executable + " -m " + model_path + " -f " + wav_path;
    std::string transcript = run_command(command);
    if (transcript.empty()) {
        std::cerr << "Transcription failed or produced no output for: " << wav_path << std::endl;
    }
    return transcript;
}

int main() {
    std::string folder_path = "F:/ytvid";
    std::string model_path = "F:/whisper.cpp/models/ggml-medium.en.bin";
    std::string whisper_cpp_path = "F:/whisper.cpp";
    std::string ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe";

    for (const auto& entry : fs::directory_iterator(folder_path)) {
        if (entry.path().extension() == ".mp4") {
            std::string video_path = entry.path().string();
            std::string wav_path = convert_video_to_wav(video_path, ffmpeg_path);
            std::string transcript = transcribe_video(wav_path, model_path, whisper_cpp_path);

            std::string txt_filename = video_path.substr(0, video_path.size() - 4) + ".txt";
            std::ofstream txt_file(txt_filename);
            if (txt_file.is_open()) {
                txt_file << transcript;
                txt_file.close();
                if (transcript.empty()) {
                    std::cerr << "Note: Saving empty transcript for " << video_path << std::endl;
                }
            } else {
                std::cerr << "Failed to open file for writing: " << txt_filename << std::endl;
            }
        }
    }
    return 0;
}
