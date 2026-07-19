#include "digest.hpp"

#include <openssl/evp.h>

#include <algorithm>
#include <iomanip>
#include <sstream>
#include <string>

namespace cc::util {

std::string sha256_hex(const std::string& data) {
  unsigned char hash[EVP_MAX_MD_SIZE];
  unsigned int len = 0;
  EVP_MD_CTX* ctx = EVP_MD_CTX_new();
  EVP_DigestInit_ex(ctx, EVP_sha256(), nullptr);
  EVP_DigestUpdate(ctx, data.data(), data.size());
  EVP_DigestFinal_ex(ctx, hash, &len);
  EVP_MD_CTX_free(ctx);
  std::ostringstream out;
  for (unsigned int i = 0; i < len; ++i) {
    out << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(hash[i]);
  }
  return out.str();
}

std::string chain_fold(const std::vector<std::string>& parts) {
  std::vector<std::string> sorted = parts;
  std::sort(sorted.begin(), sorted.end());
  std::string joined;
  for (std::size_t i = 0; i < sorted.size(); ++i) {
    if (i) {
      joined.push_back(';');
    }
    joined.append(sorted[i]);
  }
  const std::string full = sha256_hex(joined);
  return full.substr(0, 16);
}

}  // namespace cc::util
