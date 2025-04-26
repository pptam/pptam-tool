package config.repository;

import config.domain.Config;
import org.springframework.data.repository.CrudRepository;

import java.util.List;


public interface ConfigRepository extends CrudRepository<Config, String> {
    Config findByName(String name);
    List<Config> findAll();
    void deleteByName(String name);
}
