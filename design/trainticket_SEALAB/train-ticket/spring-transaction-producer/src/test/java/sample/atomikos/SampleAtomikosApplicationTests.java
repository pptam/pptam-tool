

package sample.atomikos;

import org.assertj.core.api.Condition;
import org.junit.Rule;
import org.junit.Test;

import org.springframework.boot.test.rule.OutputCapture;

import static org.assertj.core.api.Assertions.assertThat;


public class SampleAtomikosApplicationTests {

	@Rule
	public OutputCapture outputCapture = new OutputCapture();

	@Test
	public void testTransactionRollback() throws Exception {
		SampleAtomikosApplication.main(new String[] {});
		String output = this.outputCapture.toString();
		assertThat(output).has(substring(1, "---->"));
		assertThat(output).has(substring(1, "----> josh"));
		assertThat(output).has(substring(2, "Count is 1"));
		assertThat(output).has(substring(1, "Simulated error"));
	}

	private Condition<String> substring(final int times, final String substring) {
		return new Condition<String>(
				"containing '" + substring + "' " + times + " times") {

			@Override
			public boolean matches(String value) {
				int i = 0;
				while (value.contains(substring)) {
					int beginIndex = value.indexOf(substring) + substring.length();
					value = value.substring(beginIndex);
					i++;
				}
				return i == times;
			}

		};
	}

}
