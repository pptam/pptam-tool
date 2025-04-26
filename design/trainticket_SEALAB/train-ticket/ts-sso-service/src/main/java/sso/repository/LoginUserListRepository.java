package sso.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import sso.domain.LoginValue;
import java.util.ArrayList;

@Repository
public interface LoginUserListRepository extends MongoRepository<LoginValue, String> {

    @Query("{ 'id': ?0 }")
    LoginValue findById(String id);

    @Query("{ 'loginToken': ?0 }")
    LoginValue findByloginToken(String loginToken);

    ArrayList<LoginValue> findAll();

}