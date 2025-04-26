package config.service;

import config.domain.Config;
import config.domain.Information;
import config.domain.Information2;
import org.springframework.http.HttpHeaders;

import java.util.List;

public interface ConfigService {
    String create(Information info, HttpHeaders headers);
    String update(Information info, HttpHeaders headers);
    Config retrieve(Information2 info, HttpHeaders headers);
    String query(Information2 info, HttpHeaders headers);
    String delete(Information2 info, HttpHeaders headers);
    List<Config> queryAll(HttpHeaders headers);
}
