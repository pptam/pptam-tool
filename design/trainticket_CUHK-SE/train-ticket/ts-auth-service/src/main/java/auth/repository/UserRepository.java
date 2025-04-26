package auth.repository;

import auth.entity.User;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;
import java.util.UUID;

/**
 * @author fdse
 */
public interface UserRepository extends CrudRepository<User, String> {

    /**
     * find by username
     *
     * @param username username
     * @return Optional<User>
     */
    Optional<User> findByUsername(String username);

    /**
     * delete by user id
     *
     * @param userId user id
     * @return null
     */
    void deleteByUserId(String userId);
}
